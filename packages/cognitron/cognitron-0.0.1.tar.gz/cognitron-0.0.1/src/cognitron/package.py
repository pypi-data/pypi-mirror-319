import importlib


class LazyPackageData:
	def __init__(self, name):
		self.name = name
		self.module = None

	def ensure_import(self):
		if self.module is None:
			try:
				self.module = importlib.import_module(self.name)
			except ImportError:
				raise ImportError(
					f"You triggered a computation that relies on the additional package '{self.name}', which is not "
					f"installed. Please install it using 'pip install {self.name}'."
				)
		return self.module


class LazyPackage:
	def __init__(self, package_name):
		self._data = LazyPackageData(package_name)

	def __getattr__(self, name):
		data = object.__getattribute__(self, "_data")
		return getattr(data.ensure_import(), name)


def lazy_import(package_name: str):
	return LazyPackage(package_name)


def ensure_import(package_name: str):
	LazyPackageData(package_name).ensure_import()
