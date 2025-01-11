import numpy as np

from .marimo import Tree


class Point(Tree):
	__slots__ = 'x', 'y'

	def __init__(self, *args):
		super().__init__()
		if len(args) == 2:
			x, y = args
		elif len(args) == 1:
			xy = args[0]
			if isinstance(xy, (tuple, list)):
				x, y = xy
			elif isinstance(xy, np.ndarray):
				x, y = xy.tolist()
			elif isinstance(xy, Point):
				x = xy.x
				y = xy.y
			else:
				raise ValueError(f"{xy} is not a Point")
		else:
			raise ValueError("expected (x, y) or a list")

		self.x = x
		self.y = y

	def __repr__(self):
		return f"Point({self.x}, {self.y})"

	def json(self):
		return {
			"x": self.x,
			"y": self.y
		}


class Box(Tree):
	__slots__ = 'min', 'max'

	def __init__(self, *args):
		super().__init__()
		if len(args) == 4:
			self.min = Point((args[0], args[1]))
			self.max = Point((args[2], args[3]))
		elif len(args) == 2:
			self.min = Point(args[0])
			self.max = Point(args[1])
		elif len(args) == 1:
			xyxy = args[0]
			if isinstance(xyxy, Box):
				self.min = xyxy.min
				self.max = xyxy.max
			else:
				self.min = Point(xyxy[:2])
				self.max = Point(xyxy[2:4])
		else:
			raise ValueError("expected (min, max) or (minx, miny, maxx, maxy")

	def __repr__(self):
		return f"Box(min={self.min}, max={self.max})"

	def json(self):
		return {
			"min": self.min.json(),
			"max": self.max.json()
		}

	@property
	def width(self):
		return self.max.x - self.min.x

	@property
	def height(self):
		return self.max.y - self.min.y

	@property
	def xyxy(self):
		return [self.min.x, self.min.y, self.max.x, self.max.y]


class KeyPoint(Point):
	__slots__ = 'x', 'y', 'score'

	def __init__(self, xy, score: float):
		super().__init__(xy)
		if np.isnan(score):
			score = None
		self.score = score

	def __repr__(self):
		return f"KeyPoint(x={self.x}, y={self.y}, score={self.score})"

	def json(self):
		return {
			"x": self.x,
			"y": self.y,
			"score": self.score
		}
