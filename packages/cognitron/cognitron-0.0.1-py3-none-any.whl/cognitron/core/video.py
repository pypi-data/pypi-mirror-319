from __future__ import annotations

import numpy as np
import collections
import matplotlib.pyplot as plt

from pathlib import Path
from multiprocessing.pool import ThreadPool

from cognitron.core.image import Image, fig2svg, AnnotationRef
from cognitron.core.annotation import Annotation
from cognitron.core.utils import example_path
from cognitron.pipeline.device import num_cpu_cores
from cognitron.package import lazy_import


av = lazy_import("av")


class VideoFrameAnnotation(Annotation):
	def __init__(self, name: str, image: Image, file: VideoFile, time: float, picture_type: str | None):
		super().__init__(name, image)
		self._file = file
		self._time = time
		self._picture_type = picture_type

	@property
	def priority(self):
		return 100

	@property
	def video(self) -> Video:
		return Video(self._file)

	@property
	def time(self) -> float | None:
		return self._time

	@property
	def picture_type(self) -> str | None:
		return self._picture_type


class EmptyDepot:
	@property
	def pipelines(self):
		return []


class VideoFile:
	def __init__(self, path: str | Path):
		self._path = Path(path)
		self._depot = None

		with av.open(self._path, "r") as f:
			s = f.streams.video[0]
			self._width = s.width
			self._height = s.height
			self._duration = f.duration / av.time_base

	@property
	def streams(self):
		with av.open(self._path, "r") as f:
			return list(f.streams)

	@property
	def depot(self):
		if self._depot is None:
			self._depot = None
		if self._depot is None:
			return EmptyDepot()
		return self._depot

	@property
	def path(self):
		return self._path

	@property
	def aspect_ratio(self) -> float:
		return self._width / self._height

	@property
	def duration(self) -> float:
		return self._duration

	def extract_frame(self, t: float, stream=0, size=None):
		frames = collections.deque()

		with av.open(self._path, "r") as f:
			s = f.streams.video[stream]

			f.seek(
				int(t / s.time_base) + s.start_time,
				stream=s,
				backward=True)

			for frame in f.decode(s):
				frames.append(frame)
				if frame.time >= t:
					break
				while len(frames) > 2:
					frames.popleft()

		best_frame = None
		if len(frames) > 0:
			i = np.argmin(np.abs(t - np.array([x.time for x in frames])))
			best_frame = frames[i]

		r = None
		if best_frame is not None:
			r = Image.from_av(best_frame, [AnnotationRef(
					"video-frame",
					VideoFrameAnnotation,
					dict(
						file=self,
						time=best_frame.time,
						picture_type=str(best_frame.pict_type)
					))])

		if r is not None and size is not None:
			r = r.resize(size)

		return r


class VideoPlot:
	def __init__(self, video, rows=1, xticks=True):
		dpi = 250
		width = 10
		cols = 8
		grid = video.grid(int(dpi * width), cols=cols)

		fig, axs = plt.subplots(
			nrows=rows,
			gridspec_kw={'wspace': 0, 'hspace': 0},
			subplot_kw=dict(frameon=False),
			figsize=(width, rows * width / grid.aspect_ratio + rows * 0.5),
			dpi=dpi,
			sharex=True)

		self.fig = fig
		self.axs = axs

		if rows > 1:
			for ax in self.axs:
				ax.grid(which='major', axis='x', zorder=1.0)

		if rows == 1:
			ax = axs
		else:
			ax = axs[0]
		self.rows = rows

		h = (video.stop - video.start) / grid.aspect_ratio
		ax.set_xlim(video.start, video.stop)
		ax.set_ylim(0, h)

		ax.imshow(grid.pixels(), vmin=0, vmax=255, extent=(video.start, video.stop, 0, h), aspect='equal', zorder=2)

		ax.locator_params(axis='x', nbins=cols * 2)
		ax.minorticks_on()

		if xticks:
			ax.tick_params(axis='x', which='both', top=True, labeltop=True, bottom=False, labelbottom=False)
			ax.tick_params(axis='x', labelsize=10)
		else:
			ax.set_xticks([])

		ax.set_yticks([])

		ax.spines['top'].set_visible(xticks)

	# ax.spines['right'].set_visible(False)
	# ax.spines['bottom'].set_visible(False)
	# ax.spines['left'].set_visible(False)

	def close(self):
		# self.fig.subplots_adjust(hspace=.0)
		if self.rows > 1:
			self.axs[0].sharex(self.axs[1])
		self.fig.tight_layout()
		# fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
		plt.close()
		return self.fig


class Video:
	def __init__(self, file, start: float | None = None, stop: float | None = None, tracks=None):
		self._file = file
		self._start = start or 0
		self._stop = stop or file.duration
		self._tracks = tracks or []

	@staticmethod
	def open(path: str | Path):
		return Video(VideoFile(path))

	@staticmethod
	def example(path: str | Path):
		return Video.open(example_path(path))

	def view(self, start, stop):
		return Video(self._file, self._start + start, self._start + stop, self._tracks)

	@property
	def start(self):
		return self._start

	@property
	def stop(self):
		return self._stop

	@property
	def duration(self) -> float:
		return self._stop - self._start

	@property
	def streams(self):
		return self._file.streams

	@property
	def depot(self):
		return self._file.depot

	def extract_frame(self, t: float, stream=0, size=None):
		image = self._file.extract_frame(self._start + t, stream, size)
		for track in self._tracks:
			ann = track.annotation(t)
			if ann is not None:
				image = image.annotate(ann)
		return image

	def extract_frames(self, ts: list[float] | np.ndarray, stream: int = 0, size=None):
		unique, indices = np.unique(ts, return_inverse=True)
		t2i = dict((t, i) for i, t in enumerate(unique))
		frames = dict()

		with ThreadPool(min(len(unique), num_cpu_cores())) as pool:
			def f(t):
				return t, self.extract_frame(t, stream=stream, size=size)

			for t, frame in pool.imap_unordered(f, unique):
				frames[t2i[t]] = frame

		return [frames[i] for i in indices]

	@property
	def aspect_ratio(self) -> float:
		return self._file.aspect_ratio

	def grid(self, width=1280, padding=0.02, cols=8):
		box_width = width // cols
		t_width = max(box_width - int(padding * (width / cols)), 0)

		s_height = int(t_width / self.aspect_ratio)

		ts = np.linspace(0, self.duration, cols + 1)
		ts = (ts[1:] + ts[:-1]) / 2
		frames = self.extract_frames(ts, size=(t_width, s_height))

		def elements():
			xs = np.linspace(0, width - t_width, cols).round().astype(np.int32)
			for i, im in enumerate(frames):
				yield (xs[i], 0), im

		return Image.compose(
			frames[0].colorspace, (width, s_height),
			elements(),
			color="white"
		)

	def _plot(self):
		plot = VideoPlot(self)
		return plot.close()

	def _repr_svg_(self):
		return fig2svg(self._plot())

	@property
	def prepared_pipelines(self):
		return self.depot.pipelines

	def plot(self):
		return self._plot()


Video.__module__ = 'cognitron'
