import numpy as np

from cognitron.core.annotation import Annotation
from cognitron.pipeline.device import Device
from cognitron.core.utils import ensure_suffix
from cognitron.core.embedding import Embedding

from .meta import pipeline_id
from .options import Options


class FaceEmbeddingAnnotation(Annotation):
	name = pipeline_id

	def __init__(self, embedding: np.ndarray, **kwargs):
		super().__init__(**kwargs)
		self._embedding = embedding

	def json(self):
		return {
			"embedding": self._embedding.tolist()
		}

	@property
	def embedding(self):
		return Embedding(self._embedding)


def create_pipeline(options: Options, device: Device):
	from .arcface import ArcFace
	options.the_model_id = ensure_suffix(options.the_model_id, ".onnx")
	return ArcFace(options, device)


def export_hooks():
	return {
		'runtime': 'onnx',
		'options': Options,
		'pipeline': create_pipeline,
		'annotation': FaceEmbeddingAnnotation,
		'track': None
	}
