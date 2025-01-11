import contextlib

from cognitron.package import lazy_import


mo = lazy_import("marimo")


def in_marimo():
	try:
		return mo.running_in_notebook()
	except ImportError:
		return False


class DummySpinner:
	def update(self, title):
		pass


@contextlib.contextmanager
def spinner(title: str = ""):
	if in_marimo():
		with mo.status.spinner(title=title) as sp:
			yield sp
	else:
		yield DummySpinner()


class Tree:
	def __init__(self):
		pass

	def __len__(self):
		return len(self.json())

	def __getitem__(self, key):
		return self.json()[key]

	def json(self):
		raise NotImplementedError()

	def _display_(self):
		if in_marimo():
			return mo.tree(self.json())
		else:
			return None
