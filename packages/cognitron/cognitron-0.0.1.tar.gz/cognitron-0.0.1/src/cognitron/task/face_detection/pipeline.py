import PIL.Image
import numpy as np

from cognitron.core.image import AnnotationRef
from cognitron.core.annotation import ItemAnnotation, Item
from cognitron.core.utils import ensure_suffix
from cognitron.pipeline.device import Device

from .options import Options


class Face(Item):
	def __init__(self, image, data, index):
		super().__init__(data, index)
		self._image = image

	def image(
		self,
		size: tuple[int, int] | int = (112, 112),
		resample=PIL.Image.Resampling.BICUBIC,
		normalize=True,
		annotate=True):

		scale = np.array(self._image.size, dtype=np.float64)

		if isinstance(size, (int, float)):
			size = (int(size), int(size))

		if not normalize:
			xyxy = self._data.xyxy_s[self._index, :4].reshape((-1, 2, 2)) * scale
			return self._image.crop(tuple(xyxy.tolist())).resize(
				size, resample=PIL.Image.Resampling.HAMMING)
		else:
			from .transform import umeyama, TEMPLATE

			size_np = np.array(size, dtype=np.float32)
			t_scale = size_np / 112
			template = TEMPLATE * t_scale

			key_xy_src = self._data.key_xy_s[self._index, :, :2] * scale

			base = self._image.wipe()

			matrix = umeyama(
				key_xy_src,
				template,
				estimate_scale=True)

			out = base.affine(size, matrix[:2, :], resample=resample)

			if annotate:
				pts = key_xy_src
				ones = np.ones((pts.shape[0], 1))
				pts3 = np.hstack([pts, ones])

				key_xy_dst = (pts3 @ matrix.T)[:, :2]
				key_xy_dst_norm = key_xy_dst / size_np

				nans = np.zeros((key_xy_dst_norm.shape[0], 1))
				nans.fill(np.nan)
				key_xy_s_dst = np.hstack([key_xy_dst_norm, nans])

				xyxy_s = np.array([0, 0, 1, 1, self._data.xyxy_s[self._index, 4]])

				out = out.annotate(AnnotationRef("face-keypoints", ItemAnnotation, dict(
					xyxy_s=xyxy_s[np.newaxis, :],
					key_xy_s=key_xy_s_dst[np.newaxis, :])))

			return out

	def embedding(self, recognition_pipeline):
		im = recognition_pipeline(self.image())
		return im.annotations["face-recognition"].embedding


class FaceAnnotation(ItemAnnotation):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def _make_item(self, i: int):
		return Face(self._image, self._data, i)


def create_pipeline(options: Options, device: Device):
	from .scrfd import SCRFD
	options.the_model_id = ensure_suffix(options.the_model_id, ".onnx")
	return SCRFD(options, device)


def export_hooks():
	return {
		'runtime': 'onnx',
		'options': Options,
		'pipeline': create_pipeline,
		'annotation': FaceAnnotation.from_pipeline_data,
		'track': None
	}
