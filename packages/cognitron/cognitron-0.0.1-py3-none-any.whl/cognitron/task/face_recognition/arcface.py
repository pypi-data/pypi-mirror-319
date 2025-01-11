import numpy as np

from cognitron.pipeline.accelerator import Pipeline
from cognitron.pipeline.device import Device
from cognitron.core import hub
from cognitron.core.image import Image
from cognitron.package import lazy_import

from .options import Options


onnxruntime = lazy_import("onnxruntime")


class ArcFace(Pipeline):
	def __init__(self, options: Options, device: Device):
		super().__init__(options, device=device)

		model_path = hub.load(options.the_model_id)

		self._session = onnxruntime.InferenceSession(
			model_path, providers=device.onnx_providers)

		self._in_names = [x.name for x in self._session.get_inputs()]
		self._out_names = [x.name for x in self._session.get_outputs()]

	def __call__(self, message: dict):
		return [self.process(x) for x in message["images"]]

	def process(self, im: Image):
		y = np.array([im.pixels("sRGB")])
		y = np.transpose(((y - 127.5) / 128.0).astype(np.float32), (0, 3, 1, 2))
		net_outs = self._session.run(self._out_names, {self._in_names[0]: y})
		return {
			'embedding': net_outs[0][0]
		}
