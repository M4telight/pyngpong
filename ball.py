import pymlgame
from misc import Point

class Ball(object):
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.surface = pymlgame.Surface(1, 1)
        self.surface.draw_dot((0, 0), pymlgame.GREEN)

    def update(self):
        """
        Update the position of the ball for the next update, considering current
        x, y, and velocity v.
        """
        self.position += self.velocity

    def reflect(self, axis):
        """
        Adjust velocity as if the ball is reflected on a paddle.
        """
        if axis == "x":
            self.velocity = Point(-self.velocity.x, self.velocity.y)
        elif axis == "y":
            self.velocity = Point(self.velocity.x, -self.velocity.y)
        else:
            print("Warning: unknown reflection axis '{}'".format(axis))
