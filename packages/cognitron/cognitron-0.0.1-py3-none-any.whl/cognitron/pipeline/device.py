from functools import cache, lru_cache
from cognitron.package import lazy_import

torch = lazy_import("torch")
onnxruntime = lazy_import("onnxruntime")


@cache
def num_cpu_cores():
	import os
	import sys
	if sys.version_info >= (3, 13):
		return os.process_cpu_count()
	else:
		return os.cpu_count()


class Device:
	def __init__(self, code):
		self._code = code

	@property
	def onnx_providers(self):
		match self._code:
			case "cpu":
				return ["CPUExecutionProvider"]
			case "cuda":
				return ["CUDAExecutionProvider"]
			case "mps":
				return ["CoreMLExecutionProvider"]
			case x:
				raise ValueError(f"illegal device code {x}")

	@staticmethod
	@lru_cache(4)
	def best(runtime: str, exclude: tuple[str] | None = None):
		if exclude is None:
			exclude = []

		available = []

		match runtime:
			case "onnx":
				providers = set(onnxruntime.get_available_providers())

				if "CUDAExecutionProvider" in providers:
					available.append("cuda")
				if "CoreMLExecutionProvider" in providers:
					available.append("mps")

				onnxruntime.set_default_logger_severity(3)

			case "torch":
				if torch.cuda.is_available():
					available.append("cuda")
				if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
					available.append("mps")

			case x:
				raise ValueError(f"illegal runtime {x}")

		f_available = [x for x in available if x not in exclude]
		return Device(f_available[0] if f_available else "cpu")
