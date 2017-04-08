import pymlgame

from misc import Point

class Paddle:

    ALLOWED_MOVEMENT = Point(x=0, y=1)

    def __init__(self, player_id, screen, is_first_player=True):
        self.player_id = player_id
        self.surface = pymlgame.Surface(1, 3)
        self.surface.draw_line((0, 0), (0, 2), pymlgame.RED)

        self.screen = screen

        middle = self.screen.height // 2 - 1
        self.position = Point(x=0, y=middle) if is_first_player else Point(self.screen.width - 1, middle)

    def move_up(self):
        self.position += self.ALLOWED_MOVEMENT

    def move_down(self):
        self.position -= self.ALLOWED_MOVEMENT
