from collections import namedtuple

import pygame


class Point(namedtuple('Point', 'x y')):
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Point(0, 0) - self


class PygameSurfaceDecorator:
    """
    A wrapper class around pygame surfaces that monkey patches differences
    between pymlgame and pygame
    """

    def __getattribute__(self, item):
        """
        method that tries to first return method of decorator.
        If that method is not present this methods tries to return
        the property from the decorated object.
        """
        try:
            v = object.__getattribute__(self, item)
        except AttributeError:
            v = getattr(object.__getattribute__(self, 'surface'), item)
        return v

    def __init__(self, surface):
        self.surface = surface

    @property
    def width(self):
        return self.surface.get_width()

    @property
    def height(self):
        return self.surface.get_height()

    @property
    def matrix(self):
        return pygame.surfarray.array3d(self.surface)
