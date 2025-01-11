from __future__ import annotations

import numpy as np


class Embedding:
	def __init__(self, v: np.ndarray):
		self._v = v
		self._v_norm = v / np.linalg.norm(v)

	@property
	def array(self):
		return self._v

	def distance_to(self, other: Embedding):
		return 1 - self.affinity_to(other)

	def affinity_to(self, other: Embedding):
		d = np.dot(self._v_norm, other._v_norm)
		return 0.5 * d + 0.5

	def nearest(self, embeddings: list[Embedding]):
		ys = [self.affinity_to(x) for x in embeddings]
		i = np.argmax(ys)
		return i, ys[i]

	def _display_(self):
		import matplotlib.pyplot as plt
		embedding_2d = self._v.reshape(1, -1)
		fig, ax = plt.subplots(figsize=(12, 0.5))
		plt.imshow(embedding_2d, aspect='auto', cmap='gist_yarg')
		ax.spines['top'].set_visible(False)
		ax.spines['right'].set_visible(False)
		ax.spines['bottom'].set_visible(False)
		ax.spines['left'].set_visible(False)
		plt.yticks([])
		plt.close()
		return fig
