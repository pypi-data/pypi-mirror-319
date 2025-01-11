from __future__ import annotations

import numpy as np

from functools import cache, cached_property
from .image import Image
from .marimo import Tree
from .geometry import Point, KeyPoint, Box


class Annotation(Tree):
	def __init__(self, name: str, image: Image, metadata: dict | None = None):
		super().__init__()
		self._name = name
		self._image = image

	def json(self):
		return None

	@property
	def name(self) -> str:
		return self._name

	@property
	def image(self) -> Image:
		return self._image

	@property
	def priority(self):
		return 0

	@property
	def time(self) -> float | None:
		return None

	@property
	def render_options(self):
		return dict()

	@property
	def wants_colorbar(self):
		return False

	def transform(self, m: np.ndarray) -> Annotation:
		return self

	def plot(self, fig, ax, options):
		pass


class ItemData:
	labels: list[str] | None
	xyxy_s: np.ndarray | None
	key_xy_s: np.ndarray | None
	polygons: np.ndarray | None


class Item(Tree):
	def __init__(self, data: ItemData, index: int):
		super().__init__()
		self._data = data
		self._index = index

	@cache
	def json(self):
		return {
			"label": self.label,
			"bbox": self.bbox.json(),
			"score": self.score,
			"key_points": [x.json() for x in self.key_points]
		}

	@property
	def label(self) -> str | None:
		labels = self._data.labels
		return labels[self._index] if labels else None

	@property
	def bbox(self) -> Box:
		xyxy = self._data.xyxy_s[self._index, :4]
		return Box(xyxy[:2], xyxy[2:4])

	@property
	def score(self) -> float | None:
		score = self._data.xyxy_s[self._index, 4]
		return None if np.isnan(score) else score

	@property
	def key_points(self) -> list[KeyPoint]:
		key_xy_s = self._data.key_xy_s
		if key_xy_s is None:
			return []
		else:
			return [
				KeyPoint(Point(xy_s[:2]), xy_s[2])
				for xy_s in key_xy_s[self._index]]


class ItemAnnotation(Annotation):
	def __init__(
			self,
			name: str,
			image: Image,
			labels: list[str] | None = None,
			xyxy_s: np.ndarray | None = None,
			key_xy_s: np.ndarray | None = None,
			polygons: np.ndarray | None = None):

		super().__init__(name, image)

		if xyxy_s is not None and xyxy_s.size < 1:
			xyxy_s = None
		if key_xy_s is not None and key_xy_s.size < 1:
			key_xy_s = None

		if key_xy_s is not None and xyxy_s is None:
			raise ValueError("cannot use key_xy_s without xyxy_s")

		data = ItemData()
		data.labels = labels
		data.xyxy_s = xyxy_s
		data.key_xy_s = key_xy_s
		data.polygons = polygons

		self._data = data

	def json(self):
		return [x.json() for x in self.tolist()]

	@property
	def _labels(self):
		return self._data.labels

	@property
	def _xyxy_s(self):
		return self._data.xyxy_s

	@property
	def _key_xy_s(self):
		return self._data.key_xy_s

	def _make_item(self, i: int):
		return Item(self._data, i)

	def __len__(self) -> int:
		if self._xyxy_s is not None:
			return int(self._xyxy_s.shape[0])
		else:
			return 0

	def __getitem__(self, i: int):
		if 0 <= i < len(self):
			return self._make_item(i)
		else:
			raise IndexError

	def tolist(self):
		return [self._make_item(i) for i in range(len(self))]

	def __repr__(self) -> str:
		return repr(self.tolist())

	@classmethod
	def from_pipeline_data(cls, metadata, **kwargs):
		if "labels" in kwargs:
			classes = metadata["classes"]
			kwargs["labels"] = [classes[i] for i in kwargs["labels"]]
		return cls(**kwargs)

	@classmethod
	def from_track_data(cls, **kwargs):
		return cls(**kwargs)

	@cached_property
	def wants_colorbar(self):
		if self._xyxy_s is not None and not np.all(np.isnan(self._xyxy_s[:, 4])):
			return True
		elif self._key_xy_s is not None and not np.all(np.isnan(self._key_xy_s[:, :, 2])):
			return True
		else:
			return False

	def plot(self, fig, ax, options):
		from matplotlib.patches import Rectangle

		cmap = options["cmap"]
		use_cmap = self.wants_colorbar

		fontsize = 12
		size = np.array(self.image.size, dtype=np.float64)

		if self._xyxy_s is not None:
			xyxy = self._xyxy_s[:, :4].reshape(-1, 2, 2) * size

			for i, ((min_x, min_y), (max_x, max_y)) in enumerate(xyxy):
				confidence = self._xyxy_s[i, 4]
				if np.isnan(confidence):
					confidence = 1

				label = self._labels[i] if self._labels else None
				if label is None:
					label = "%.2f" % confidence

				color = cmap(confidence) if use_cmap else (1, 0, 0)

				ax.add_patch(Rectangle(
					(min_x, min_y),
					max_x - min_x, max_y - min_y,
					edgecolor="none", facecolor="white",
					linewidth=0, alpha=0.2))

				lw = min(2, max(1, min(max_x - min_x, max_y - min_y) / 100))

				ax.add_patch(Rectangle(
					(min_x, min_y),
					max_x - min_x, max_y - min_y,
					edgecolor=color, facecolor="none",
					linewidth=lw, alpha=1))

				if label:
					ax.text(
						min_x, min_y, label, color='w', weight='normal',
						fontsize=fontsize, ha='left', va='top',
						bbox=dict(boxstyle="square,pad=0", facecolor=color, edgecolor="none", lw=0))

		if self._key_xy_s is not None:
			if self._xyxy_s is not None:
				figsize = options["figsize"]
				pt = options["dpi"] / 72
				xyxy = self._xyxy_s[:, :4].reshape(-1, 2, 2) * np.array(figsize)
				diff = xyxy[:, 1, :] - xyxy[:, 0, :]
				pt_scale = max(1 / pt, np.mean(diff[:, 0] * diff[:, 1]) / (figsize[0] * figsize[1]))
			else:
				pt_scale = 1

			for i in range(self._key_xy_s.shape[0]):
				item = self._key_xy_s[i]
				if np.all(np.isnan(item[:, 2])):
					colors = ["w"] * item.shape[0]
				else:
					colors = [cmap(x) for x in item[:, 2]]

				xy = item[:, :2] * size

				ax.scatter(xy[:, 0], xy[:, 1], c=colors, s=pt_scale * 2.5)
				ax.scatter(xy[:, 0], xy[:, 1], c="white", s=pt_scale * 0.5)
