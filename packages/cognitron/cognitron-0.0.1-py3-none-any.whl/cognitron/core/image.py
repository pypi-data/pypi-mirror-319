from __future__ import annotations as __annotations__

import numpy as np
import PIL.Image
import io
import re
import colour
import typing

from functools import lru_cache, cache, cached_property
from pathlib import Path

from cognitron.package import lazy_import, ensure_import
from cognitron.core.marimo import spinner, Tree
from cognitron.core.utils import example_path


def pixels_to_float(x):
	if x.dtype.kind == 'f':
		return x
	else:
		return x / np.float32(255)


def pixels_to_uint8(x):
	if x.dtype.kind == 'f':
		return np.rint(x.clip(0, 1) * 255).astype(np.uint8)
	else:
		return x.astype(np.uint8)


def pixels_to_dtype(x, dtype):
	match np.dtype(dtype).name:
		case "uint8": return pixels_to_uint8(x)
		case "float32": return pixels_to_float(x).astype(np.float32)
		case "float64": return pixels_to_float(x).astype(np.float64)
		case _: raise ValueError(x)


def figsize_dpi(px_width, px_height, max_figsize, dpi=75, scale=1):
	aspect_ratio = px_width / px_height

	inch_w = min(max_figsize[0], px_width / dpi)
	inch_h = min(max_figsize[1], inch_w / aspect_ratio)
	inch_w = inch_h * aspect_ratio

	figsize = (inch_w * scale, inch_h * scale)
	return dict(dpi=dpi, figsize=figsize)


def fig2png(fig):
	with io.BytesIO() as buf:
		fig.savefig(buf, format='png')
		return buf.getvalue()


def fig2svg(fig):
	with io.BytesIO() as buf:
		fig.savefig(buf, format='svg')
		return buf.getvalue().decode('utf8')


class StandardTransferFunction:
	def __init__(self, gamma: str):
		self.eotf = colour.models.EOTFS[gamma]
		self.eotf_inverse = colour.models.EOTF_INVERSES[gamma]


class Colorspace:
	def __init__(self, name: str):
		if name == "sRGB":
			name = "non-linear RGB (sRGB)"

		m = re.match(r"non-linear (\w+) (\([^)]+\))?", name)

		if m is None:
			self._mode = name
			self._gamma = None
		else:
			self._mode = m.group(1)
			self._gamma = m.group(2)[1:-1]

		if self._mode not in Colorspace.modes():
			raise ValueError(f"illegal color mode '{self._mode}'")

		if self._gamma is None:
			self._tf = None
		else:
			self._tf = StandardTransferFunction(self._gamma)

	def __eq__(self, other):
		return isinstance(other, Colorspace) and self.name == other.name

	@property
	def mode(self):
		return self._mode

	@property
	def is_gamma_compressed(self):
		return self._tf is not None

	@cached_property
	def name(self):
		if self._gamma is None:
			return self._mode
		else:
			return f"non-linear {self._mode} ({self._gamma})"

	def eotf(self, x):
		return self._tf.eotf(x) if self._tf else x

	def eotf_inverse(self, x):
		return self._tf.eotf_inverse(x) if self._tf else x

	@staticmethod
	@cache
	def modes():
		return set(colour.COLOURSPACE_MODELS)


class AnnotationRef(typing.NamedTuple):
	name: str
	cls: type | callable
	options: dict


class AnnotationDict(Tree):
	def __init__(self, image: Image, ann: list[AnnotationRef]):
		super().__init__()
		self._image = image
		self._ann = ann
		self._by_name = {x.name: x for x in self._ann}

	@property
	def top(self):
		return self._create(len(self._ann) - 1)

	def __len__(self):
		return len(self._ann)

	def __getitem__(self, name: str):
		ref = self._by_name[name]
		return ref.cls(name=ref.name, image=self._image, **ref.options)

	def json(self):
		return dict((k, self[k].json()) for k in self.keys())

	def keys(self):
		return self._by_name.keys()

	def _create(self, i: int):
		ref = self._ann[i]
		return ref.cls(name=ref.name, image=self._image, **ref.options)

	def tolist(self):
		return [self._create(i) for i in range(len(self._ann))]

	def __repr__(self):
		return f"{dict((k, self[k]) for k in self.keys())}>"


class Track:
	def close(self):
		pass

	def annotate(self, t: float) -> AnnotationRef:
		raise NotImplementedError()

	def timestamps(self):
		pass


def saturate(pixels, ds):
	hsl = colour.RGB_to_HSL(pixels_to_float(pixels))
	hsl[:, :, 1] = (hsl[:, :, 1] + ds).clip(0, 1)
	return pixels_to_uint8(colour.HSL_to_RGB(hsl))


class SVG:
	def __init__(self, svg):
		self.svg = svg

	def _repr_svg_(self):
		return self.svg


class Image:
	def __init__(
			self,
			pixels: np.ndarray,
			colorspace: str = "sRGB",
			palette: np.ndarray | None = None,
			annotations: list[AnnotationRef] | None = None):

		self._pixels = pixels
		self._colorspace = Colorspace(colorspace)
		self._palette = palette
		self._ann = annotations or []

	def to_pil(self):
		return PIL.Image.fromarray(self.pixels("sRGB"))

	@staticmethod
	def open(p: str | Path):
		return Image(np.array(PIL.Image.open(p).convert("RGB")), "sRGB")

	@staticmethod
	def example(p: str | Path):
		return Image.open(example_path(p))

	@staticmethod
	def get(url: str):
		from .utils import sizeof_fmt
		import requests
		import io
		from urllib.parse import urlparse

		with spinner(f"Downloading image from {urlparse(url).netloc}.") as sp:
			response = requests.get(url)
			response.raise_for_status()
			data = response.content
			sp.update(f"Downloaded {sizeof_fmt(len(data))} from {urlparse(url).netloc}.")

		return Image.from_pil(PIL.Image.open(io.BytesIO(data)))

	@staticmethod
	def from_pil(im: PIL.Image.Image):
		return Image(np.array(im.convert("RGB")), colorspace="sRGB")

	@staticmethod
	def from_av(frame, annotations: list[AnnotationRef] | None = None):
		return Image(frame.to_ndarray(
				format='rgb24',
				dst_colorspace="itu709"),
			colorspace="non-linear RGB (ITU-R BT.1886)",
			annotations=annotations)

	def crop(self, *xyxy) -> Image:
		from .geometry import Box
		box = Box(*xyxy)

		x0, x1 = map(int, [np.floor(xyxy[0]), np.ceil(xyxy[2])])
		y0, y1 = map(int, [np.floor(xyxy[1]), np.ceil(xyxy[3])])

		return Image(
			self._pixels[y0:y1, x0:x1],
			self.colorspace, self._palette, [])

	def convert(self, colorspace: str, dtype=None):
		return Image(self.pixels(colorspace, dtype), colorspace)

	def quantize(self, colors: int | float | None = None, method: str = "kmeans", colorspace: str = "CIE Luv", **kwargs):
		sklearn = lazy_import("sklearn")

		match method:
			case "kmeans":
				algorithm = sklearn.cluster.KMeans(
					n_clusters=colors or 16, **kwargs)
			case "meanshift":
				algorithm = sklearn.cluster.MeanShift(
					bandwidth=colors or 0.05, **kwargs)
			case _:
				raise ValueError(f"unsupported method '{method}'")

		pixels = self.pixels(colorspace)
		clustering = algorithm.fit(
			pixels.reshape((-1, pixels.shape[-1])))

		n = clustering.cluster_centers_.shape[0]
		if n < 0x100:
			dtype = np.uint8
		elif n < 0x10000:
			dtype = np.uint16
		else:
			dtype = np.uint32

		return Image(
			clustering.labels_.reshape(pixels.shape[:-1]).astype(dtype),
			colorspace,
			clustering.cluster_centers_,
			self._ann)

	@staticmethod
	def compose(colorspace: str, size: tuple[int, int], elements, color="white"):
		import matplotlib
		pixels = np.empty((size[1], size[0], 3), dtype=np.uint8)
		pixels[:] = pixels_to_uint8(np.array(
			matplotlib.colors.to_rgb(color), dtype=np.float32))
		for (x, y), im in elements:
			w, h = im.size
			pixels[y:y + h, x:x + w] = im.pixels(colorspace)
		return Image(pixels, colorspace)

	def annotate(self, r: AnnotationRef):
		return Image(
			self._pixels, self.colorspace, self._palette, self._ann + [r])

	def wipe(self) -> Image:
		return Image(self._pixels, self.colorspace, self._palette)

	@property
	def top(self):
		return self.annotations.top

	@property
	def annotations(self):
		return AnnotationDict(self, self._ann)

	def box(self, *xyxy, label=None, score=None):
		from .geometry import Box
		from .annotation import ItemAnnotation
		box = Box(*xyxy)
		return self.annotate(AnnotationRef("box", ItemAnnotation, {
			"labels": [label] if label else None,
			"xyxy_s": np.array([box.xyxy + [score or np.nan]]),
			"key_xy_s": None,
			"polygons": None
		}))

	@cached_property
	def size(self):
		return self._pixels.shape[1], self._pixels.shape[0]

	@cached_property
	def width(self):
		return self._pixels.shape[1]

	@cached_property
	def height(self):
		return self._pixels.shape[0]

	@cached_property
	def aspect_ratio(self):
		return self.width / self.height

	@cached_property
	def colorspace(self) -> str:
		return self._colorspace.name

	def palette(self, colorspace: str = "sRGB"):
		return self._to_colorspace(self._palette, Colorspace(colorspace))

	@property
	def is_paletted(self):
		return self._palette is not None

	def _to_colorspace(self, pixels, colorspace: Colorspace):
		if colorspace == self._colorspace:
			return pixels
		else:
			linear = self._colorspace.eotf(pixels_to_float(pixels))
			converted = colour.convert(linear, self._colorspace.mode, colorspace.mode)
			return colorspace.eotf_inverse(converted)

	@lru_cache(2)
	def pixels(self, colorspace: str = "sRGB", dtype=None):
		if colorspace == "paletted":
			if self.is_paletted:
				return self._pixels
			else:
				raise RuntimeError("cannot get paletted pixels from non-paletted image")

		target_cs = Colorspace(colorspace)

		if self.is_paletted:
			palette = self._to_colorspace(self._palette, target_cs)

			pixels = palette[self._pixels.reshape((-1,))].reshape(
				(*self._pixels.shape, palette.shape[-1]))
		else:
			pixels = self._to_colorspace(self._pixels, target_cs)

		if dtype is None and target_cs.mode == "RGB" and target_cs.is_gamma_compressed:
			dtype = np.uint8
		if dtype is not None:
			pixels = pixels_to_dtype(pixels, dtype)

		return pixels

	def affine(self, size: tuple[int, int], matrix: np.ndarray, resample=PIL.Image.Resampling.BICUBIC):
		matrix = np.array(matrix)
		if matrix.shape != (2, 3):
			raise ValueError("matrix must be of shape (2, 3)")

		matrix_inv = np.linalg.inv(np.vstack((matrix, [0, 0, 1])))
		flat_matrix = matrix_inv[:2, :].flatten().tolist()

		width, height = size

		num_c = self._pixels.shape[-1]
		linear = self._colorspace.eotf(pixels_to_float(self._pixels))
		transformed = np.empty((height, width, num_c), dtype=np.float32)

		for i in range(num_c):
			c = PIL.Image.fromarray(linear[:, :, i])
			c = c.transform(
				(width, height),
				PIL.Image.Transform.AFFINE,
				flat_matrix,
				resample=resample)
			transformed[:, :, i] = np.array(c)

		transformed = self._colorspace.eotf_inverse(transformed)

		return Image(
			transformed,
			self.colorspace,
			self._palette)

	@lru_cache(2)
	def resize(self, size: tuple[int, int] | int, resample=None):
		if np.ndim(size) == 0:
			width = int(size)
			height = int(round(width / self.aspect_ratio))
		else:
			width, height = size

		if self.is_paletted:
			if resample is not None:
				raise ValueError("cannot specify resample for paletted images")
			if np.dtype(self._pixels.dtype).name in ('uint8', 'uint16'):
				c = PIL.Image.fromarray(self._pixels.astype(np.uint16), "I;16").resize(
					(width, height), resample=PIL.Image.Resampling.NEAREST)
			else:
				raise RuntimeError(f"failed to resize pixels of type {self._pixels.dtype}")
			resized = np.array(c)
		else:
			if resample is None:
				if width <= self.width and height <= self.height:
					resample = PIL.Image.Resampling.HAMMING
				else:
					resample = PIL.Image.Resampling.LANCZOS

			num_c = self._pixels.shape[-1]
			linear = self._colorspace.eotf(pixels_to_float(self._pixels))
			resized = np.empty((height, width, num_c), dtype=np.float32)

			for i in range(num_c):
				c = PIL.Image.fromarray(linear[:, :, i])
				c = c.resize((width, height), resample=resample)
				resized[:, :, i] = np.array(c)

			resized = self._colorspace.eotf_inverse(resized)

		return Image(
			resized,
			self.colorspace,
			self._palette)

	def save(self, p: str | Path, **kwargs):
		self.to_pil().save(p, **kwargs)

	@cache
	def _repr_png_(self):
		if not self._ann:
			with io.BytesIO() as buf:
				self.to_pil().save(buf, format="png", compress_level=0)
				return buf.getvalue()
		else:
			return None

	@cache
	def _repr_svg_(self):
		return self.plot().svg

	def plot(self, desaturate=None, legend=True, scale=1, dpi=75, cmap='YlGn'):
		import matplotlib
		import matplotlib.pyplot as plt
		from matplotlib.transforms import ScaledTranslation

		plot_kwargs = figsize_dpi(
			self.width, self.height, dpi=dpi, max_figsize=(8, 4), scale=scale)

		if scale > 1:
			interpolation = 'nearest'
		else:
			interpolation = None

		if min(plot_kwargs["figsize"]) < 1:
			legend = False

		ann = self.annotations.tolist()
		colorbar = legend and any(x.wants_colorbar for x in ann)

		options = dict()
		options["cmap"] = matplotlib.colormaps[cmap]
		options["figsize"] = plot_kwargs["figsize"]
		options["dpi"] = plot_kwargs["dpi"]

		if colorbar:
			w = 1

			figsize = plot_kwargs["figsize"]
			figsize = (
				figsize[0] + w,
				figsize[1]
			)
			plot_kwargs["figsize"] = figsize

			r = (w - 0.2) / figsize[0]

			fig, axs = plt.subplots(
				1, 2,
				gridspec_kw={'wspace': 0, 'hspace': 0},
				width_ratios=[1 - r, r],
				**plot_kwargs)
			if desaturate is None:
				desaturate = 0.2
			main_ax = axs[0]
			side_ax = axs[1]
		else:
			fig, main_ax = plt.subplots(**plot_kwargs)
			side_ax = None

		pixels = self.pixels("sRGB")
		if (desaturate or 0) > 0:
			pixels = saturate(pixels, -desaturate)
		main_ax.imshow(pixels, vmin=0, vmax=255, interpolation=interpolation)
		main_ax.axis('off')

		ts = []

		for x in sorted(ann, key=lambda x: x.priority):
			x.plot(fig, main_ax, options)

			t = x.time
			if t is not None:
				ts.append(t)

		if colorbar:
			from matplotlib import cm
			from matplotlib.colors import Normalize
			norm = Normalize(vmin=0, vmax=1)
			fig.colorbar(
				cm.ScalarMappable(norm=norm, cmap=cmap),
				ax=side_ax,
				orientation='vertical',
				fraction=1,
				shrink=0.9,
				pad=0)
			side_ax.axis('off')

		fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)

		if len(ts) >= 1:
			ts_str = " | ".join([f"{t:.2f}" for t in ts])

			padding_pixels = (16, 16)
			transform = main_ax.transAxes + ScaledTranslation(
				padding_pixels[0] / fig.dpi,
				-padding_pixels[1] / fig.dpi,
				fig.dpi_scale_trans)

			main_ax.text(
				0, 1, ts_str, transform=transform, fontsize=10, va='top', ha='left',
				bbox=dict(boxstyle="square,pad=0.4", edgecolor="black", facecolor="white", linewidth=1))

		plt.close()

		return SVG(fig2svg(fig))


Image.__module__ = 'cognitron'


class Thumbnailer:
	def __init__(self, size: int, quality: int, fmt: str = "avif"):
		self.size = size
		self.quality = quality
		self.format = fmt

		if self.format == "avif":
			ensure_import("pillow_avif")

	@property
	def media_type(self):
		return f"image/{self.format}"

	@property
	def suffix(self):
		return f".{self.format}"

	def thumbnail(self, image: Image):
		import PIL.ImageCms

		size = self.size
		w, h = image.size
		if w >= h:
			new_w = min(w, size)
			new_h = int((h / w) * new_w)
		else:
			new_h = min(h, size)
			new_w = int((w / h) * new_h)

		r = image.resize((new_w, new_h))
		im = r.to_pil()

		profile = PIL.ImageCms.createProfile("sRGB")
		icc_profile = PIL.ImageCms.ImageCmsProfile(profile).tobytes()

		with io.BytesIO() as output:
			im.save(output, format=self.format, quality=self.quality, icc_profile=icc_profile)
			return output.getvalue()
