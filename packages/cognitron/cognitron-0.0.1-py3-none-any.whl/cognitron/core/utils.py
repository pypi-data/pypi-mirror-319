import math

from typing import Iterable


def example_path(name):
	import os
	from pathlib import Path
	p = os.getenv("COGNITRON_EXAMPLES")
	if p is None:
		raise RuntimeError("COGNITRON_EXAMPLES environment variable not set")
	return Path(p) / name


def pick_architecture(model_id: str, choices: Iterable) -> str:
	for x in choices:
		k = x.value
		if k != "automatic" and model_id.startswith(k):
			return x
	raise RuntimeError(
		f"failed to detect model architecture for model '{model_id}'")


def ensure_suffix(name: str, suffix: str) -> str:
	if "." not in name:
		return name + suffix
	else:
		return name


def sizeof_fmt(num, suffix='B'):
	# taken from https://gist.github.com/cbwar/d2dfbc19b140bd599daccbe0fe925597
	magnitude = int(math.floor(math.log(num, 1024)))
	val = num / math.pow(1024, magnitude)
	if magnitude > 7:
		return '{:.1f}{}{}'.format(val, 'Yi', suffix)
	return '{:3.1f}{}{}'.format(val, ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi'][magnitude], suffix)
