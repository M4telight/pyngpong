import pymlgame
from misc import Point

def draw_p(surface, origin=Point(0, 0), color=pymlgame.RED):
    """
    Draw the letter P to the given surface. The size is 3x5.
    """
    # note(hrantzsch): we might want scaling, but ATM we don't need it
    tr = origin + Point(2, 0)  # top right
    bl = origin + Point(0, 4)

    surface.draw_line(origin, bl, color)
    surface.draw_line(tr, tr + Point(0, 2), color)
    surface.draw_dot(origin + Point(1, 0), color)
    surface.draw_dot(origin + Point(1, 2), color)

def draw_0(surface, origin=Point(0, 0), color=pymlgame.RED):
    """
    Draw the figure 0 to the given surface. The size is 3x5.
    """
    tr = origin + Point(2, 0)  # top right
    bl = origin + Point(0, 4)
    br = origin + Point(2, 4)

    surface.draw_line(origin, bl, color)
    surface.draw_line(tr, br, color)
    surface.draw_dot(origin + Point(1, 0), color)
    surface.draw_dot(bl + Point(1, 0), color)

def draw_1(surface, origin=Point(0, 0), color=pymlgame.RED):
    """
    Draw the figure 1 to the given surface. The size is 1x5.
    """
    surface.draw_line(origin, origin + Point(0, 4), color)
