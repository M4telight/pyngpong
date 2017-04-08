from collections import namedtuple


class Point(namedtuple('Point', 'x y')):
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Point(0, 0) - self
