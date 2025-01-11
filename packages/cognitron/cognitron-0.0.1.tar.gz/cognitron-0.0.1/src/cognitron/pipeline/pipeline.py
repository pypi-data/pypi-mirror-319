import importlib
import pkgutil

from functools import cache, cached_property

from cognitron.pipeline.accelerator import Pipeline
from cognitron.pipeline.device import Device
from cognitron.core.image import Image, AnnotationRef


class ImageAnnotationPipeline(Pipeline):
	def __init__(self, plugin_id: str, inner: Pipeline, annotation):
		super().__init__(inner.options, device=inner.device)
		self._plugin_id = plugin_id
		self._inner = inner
		self._annotation = annotation

	def metadata(self):
		return self._inner.metadata()

	def __call__(self, images: Image | list[Image], **kwargs):
		if isinstance(images, Image):
			images = [images]
			was_list = False
		else:
			was_list = True

		results = self._inner({
			"images": images
		}, **kwargs)
		output = [
			im.annotate(AnnotationRef(
				self._plugin_id,
				self._annotation,
				dict(
					**x, metadata=self.metadata())))
			for im, x in zip(images, results)
		]

		if not was_list:
			output = output[0]

		return output


class PipelineMeta:
	def __init__(self, plugin_id: str, module_name: str):
		self._plugin_id = plugin_id
		self._module_name = module_name

	@cached_property
	def hooks(self):
		m = importlib.import_module(self._module_name)
		return m.export_hooks()

	def raw_pipeline(self, device: str | None, **kwargs):
		if device is None:
			device = Device.best(
				self.hooks["runtime"],
				tuple(self.hooks.get("device_exclude", [])))

		options = self.hooks["options"](**kwargs)

		return self.hooks["pipeline"](options, device=device)

	def pipeline(self, device: str | None, **kwargs):
		return ImageAnnotationPipeline(
			self._plugin_id,
			self.raw_pipeline(device, **kwargs),
			self.hooks["annotation"])

	def create_track(self, entry):
		return self.hooks["track"](entry)


@cache
def load_pipelines():
	pipelines = dict()

	plugins = importlib.import_module("cognitron.task")
	for loader, name, is_pkg in pkgutil.walk_packages(plugins.__path__):
		full_name = plugins.__name__ + "." + name

		try:
			meta_module = importlib.import_module(full_name + ".meta")
			pipeline_id = meta_module.pipeline_id

			pipelines[pipeline_id] = PipelineMeta(
				pipeline_id, full_name + ".pipeline")
		except ImportError:
			pass

	return pipelines


def get_meta(name: str) -> PipelineMeta:
	pipelines = load_pipelines()
	p = pipelines.get(name)
	if p is None:
		raise ValueError(f"cognitron has no pipeline called {name}")
	return p


def raw_pipeline(name: str, device=None, **kwargs):
	return get_meta(name).raw_pipeline(
		device=device, **kwargs)


def pipeline(name: str, device=None, **kwargs):
	return get_meta(name).pipeline(
		device=device, **kwargs)


def create_track(name: str, entry):
	return get_meta(name).create_track(entry)
