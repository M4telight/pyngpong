from collections import namedtuple

import pymlgame

class Point(namedtuple('Point', 'x y')):
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)


class Paddle:

    def __init__(self, player_id, screen, is_first_player=True):
        self.player_id = player_id
        self.surface = pymlgame.Surface(1, 3)
        self.surface.draw_line((0, 0), (0, 2), pymlgame.RED)

        self.screen = screen

        middle = self.screen.height // 2 - 1
        self.position = Point(x=0, y=middle) if is_first_player else Point(self.screen.width - 1, middle)
