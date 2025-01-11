import contextlib
import multiprocessing
import signal
import logging
import threading
import io
import logging.handlers
import numpy as np

from typing import Iterable
from functools import partial
from pydantic import BaseModel
from cognitron.package import ensure_import
from cognitron.pipeline.device import num_cpu_cores, Device
from cognitron.core.image import Image


def image_batch_pixels(images: list[Image]):
	pixels = np.vstack([x.pixels("sRGB") for x in images])
	if len(images) == 1:
		pixels = np.expand_dims(pixels, axis=0)
	batch_size = pixels.shape[0]
	assert batch_size == len(images)
	return pixels


class Pipeline:
	def __init__(self, options: BaseModel, device: Device):
		if device is None:
			raise ValueError("device must not be None")
		self._options = options
		self._device = device

	@property
	def options(self) -> BaseModel:
		return self._options

	@property
	def device(self) -> Device:
		return self._device

	def unload(self):
		raise NotImplementedError()

	def metadata(self) -> dict:
		return dict()

	def __call__(self, *args, **kwargs):
		raise NotImplementedError()

	def flush(self):
		return None


def _init_work(init):
	import os
	os.environ["LOKY_MAX_CPU_COUNT"] = "1"
	signal.signal(signal.SIGINT, signal.SIG_IGN)
	if init is not None:
		init()


def _do_work(x, work):
	try:
		from threadpoolctl import threadpool_limits
		with threadpool_limits(limits=1, user_api='blas'):
			# with colour.utilities.disable_multiprocessing():
			return work(x)
	except KeyboardInterrupt as e:
		return None, []
	except Exception as e:
		logging.exception(e)
		return None, []


class CPU:
	def __init__(self, concurrency: int):
		self._concurrency = concurrency

	def imap_unordered(self, f, xs, init=None):
		concurrency = self._concurrency
		if concurrency is None:
			concurrency = num_cpu_cores()

		work = partial(_do_work, work=f)

		with multiprocessing.Pool(
				concurrency,
				initializer=partial(_init_work, init=init)) as pool:
			yield from pool.imap_unordered(
				work, xs, chunksize=2)


class Command:
	pass


class MetadataCommand(Command):
	pass


class PushCommand(Command):
	def __init__(self, key, message: dict):
		self.key = key
		self.message = message


class FlushCommand(Command):
	pass


class SentinelCommand(Command):
	pass


class StopCommand(Command):
	pass


class LogCommand(Command):
	def __init__(self, level, message: str):
		self.level = level
		self.message = message


class Printer(io.RawIOBase):
	def __init__(self, q: multiprocessing.Queue, level):
		self._q = q
		self._level = level

	def write(self, s: str):
		self._q.put(LogCommand(self._level, s))


class Response:
	pass


class Success(Response):
	def __init__(self, key, data):
		self.key = key
		self.data = data


class Failure(Response):
	def __init__(self, exc):
		self.exc = exc


class Sentinel(Response):
	pass


class LoggerWriter:
	def __init__(self, log_fn):
		self.log_fn = log_fn
		self.buf = []

	def write(self, msg):
		if msg.endswith('\n'):
			self.buf.append(msg.removesuffix('\n'))
			self.log_fn(''.join(self.buf))
			self.buf = []
		else:
			self.buf.append(msg)

	def flush(self):
		pass


class Process:
	def __init__(
		self,
		q_in: multiprocessing.Queue,
		q_out: multiprocessing.Queue,
		q_log: multiprocessing.Queue,
		pipeline_id: str,
		options: dict,
		device: str | None):

		self.q_in = q_in
		self.q_out = q_out
		self.q_log = q_log
		self.pipeline_id = pipeline_id
		self.options = options
		self.pipeline = None
		self.device = device

	def _exec(self, key, f):
		try:
			res = f()
		except Exception as e:
			logging.exception(e)
			self.q_out.put(Failure(e))
			return False
		else:
			self.q_out.put(Success(key, res))
			return True

	def run(self):
		import sys

		try:
			from .pipeline import raw_pipeline

			self.pipeline = raw_pipeline(
				self.pipeline_id,
				**self.options,
				device=self.device)
		except Exception as e:
			logging.exception(e)
			self.q_out.put(Failure(e))
			return
		else:
			self.q_out.put(Success("init", None))

		logger = logging.getLogger()
		while logger.hasHandlers():
			logger.removeHandler(logger.handlers[0])
		logger.addHandler(logging.handlers.QueueHandler(self.q_log))

		logging.captureWarnings(True)

		sys.stdout = LoggerWriter(logger.debug)
		sys.stderr = LoggerWriter(logger.warning)

		import transformers
		import importlib
		importlib.reload(transformers)

		import transformers.utils.logging
		#transformers.utils.logging.set_verbosity_error()
		transformers.utils.logging.disable_default_handler()
		transformers.utils.logging.add_handler(logging.handlers.QueueHandler(self.q_log))
		#transformers.utils.logging.captureWarnings(True)

		#logger.info("gpu process launched.")
		#transformers.utils.logging.warning_once("some warning.")
		#warnings.warn("a test warning.")
		#transformers.utils.logging.get_logger().info("transformer log test.")

		#with (
		#	contextlib.redirect_stdout(Printer(q_print, logging.DEBUG)),
		#	contextlib.redirect_stderr(Printer(q_print, logging.WARN))):

		done = False
		pipe = self.pipeline

		while not done:
			match self.q_in.get():
				case StopCommand():
					done = True
				case SentinelCommand():
					self.q_out.put(Sentinel())
				case MetadataCommand():
					self._exec(None, lambda: pipe.metadata())
				case PushCommand(key=key, message=message):
					self._exec(key, lambda: pipe(message))
				case FlushCommand():
					self._exec(None, lambda: pipe.flush())


def run_gpu(*args):
	try:
		Process(*args).run()
	except Exception as e:
		logging.exception(e)


class GPU:
	def __init__(self, pipeline_id: str, options: dict, device: str | None):
		self._pipeline_id = pipeline_id
		self._options = options
		self._device = device

		self._q_in = multiprocessing.Queue(maxsize=2)
		self._q_out = multiprocessing.Queue(maxsize=2)
		self._q_log = multiprocessing.Queue(-1)

		self._p = multiprocessing.Process(target=run_gpu, args=(
			self._q_in, self._q_out, self._q_log, pipeline_id, options, device
		))
		self._p.start()

		# wait until process has loaded, before redirecting stdout. this allows
		# huggingface hub to use tqdm during downloads.

		match self._q_out.get():
			case Success(key="init", data=_):
				pass
			case Failure(exc=exc):
				raise exc
			case x:
				raise ValueError(f"illegal reply {x}")

		import transformers.utils.logging
		transformers.utils.logging.disable_default_handler()
		transformers.utils.logging.add_handler(logging.getLogger().handlers[0])

		def print_from_q():
			while True:
				record = self._q_log.get()
				if record is None:
					break
				logger = logging.getLogger(record.name)
				logger.handle(record)

		self._printer = threading.Thread(target=print_from_q)
		self._printer.start()

		_, self.metadata = self._call(MetadataCommand())

	def _call(self, command: Command):
		self._q_in.put(command)
		match self._q_out.get():
			case Success(key=key, data=data):
				return key, data
			case Failure(exc=exc):
				raise exc

	def matches(self, pipeline_id: str, options: dict, device: str | None):
		return self._pipeline_id is pipeline_id and self._options == options and self._device == device

	def close(self):
		self._q_in.put(StopCommand())
		self._p.join()

		#self._listener.stop()

		self._q_log.put(None)
		self._printer.join()

	def once(self, message: dict):
		_, data = self._call(PushCommand(None, message))
		return data

	def stream(self, xs: Iterable[dict]):
		for key, message in xs:
			r_key, data = self._call(PushCommand(key, message))
			yield r_key, data

		if False:
			def push():
				for key, message in xs:
					self._q_in.put(PushCommand(key, message))
				self._q_in.put(SentinelCommand())

			thread = threading.Thread(target=push)
			thread.start()

			for x in self._q_out.get():
				print("??", x)
				key, r = x
				if key is SENTINEL:
					break
				yield key, r

			thread.join()

	def flush(self):
		_, data = self._call(FlushCommand())
		return data


class Accelerator:
	def __init__(self):
		self._gpu = None

	@contextlib.contextmanager
	def cpu(self, concurrency: int) -> CPU:
		ensure_import("threadpoolctl")
		yield CPU(concurrency)

	@contextlib.contextmanager
	def gpu(self, pipeline_id: str, options: dict, device: str | None) -> GPU:
		if self._gpu and not self._gpu.matches(pipeline_id, options, device):
			self.close()
		if self._gpu is None:
			self._gpu = GPU(pipeline_id, options, device)
		yield self._gpu

	def close(self):
		if self._gpu:
			self._gpu.close()
			self._gpu = None
