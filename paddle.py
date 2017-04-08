import pymlgame

from misc import Point


class Paddle:

    ALLOWED_MOVEMENT = Point(x=0, y=1)

    def __init__(self, player_id, screen, is_first_player=True):
        self.player_id = player_id
        self.paddle_height = 3
        self.surface = pymlgame.Surface(1, self.paddle_height)
        self.surface.draw_line((0, 0), (0, 2), pymlgame.RED)

        self.screen = screen

        middle = self.screen.height // 2 - 1
        self.position = Point(x=0, y=middle) if is_first_player else Point(self.screen.width - 1, middle)

    def move_up(self):
        self.position -= self.ALLOWED_MOVEMENT

        if self.position.y < 0:
            self.position = Point(x=self.position.x, y=0)

    def move_down(self):
        self.position += self.ALLOWED_MOVEMENT

        if self.position.y > self.screen.height - self.paddle_height:
            self.position = Point(x=self.position.x, y=self.screen.height - self.paddle_height)

    def check_collision(self, ball):
        x_coll = abs(self.position.x - ball.position.x) <= 1
        y_coll = self.position.y <= ball.position.y < self.position.y + self.paddle_height
        return x_coll and y_coll
