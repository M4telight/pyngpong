import pymlgame
import time

import drawing
from misc import Point


class GameState():
    """
    Abstract base class for a state of a pyngpong game. Derived classes should
    implement update() and render().
    States will go ahead and replace themselves by another state if they deem
    it necessary.
    """

    def __init__(self, game):
        self.game = game

    def update(self):
        pass

    def render(self):
        pass


class WaitingState(GameState):
    """
    In this state, the game waits for 2 players to join.
    """

    def update(self):
        if len(self.game.players) == 2:
            self.game.state = StartingState(self.game)

    def render(self):
        p0_color = pymlgame.GREEN if len(self.game.players) > 0 \
            else pymlgame.GREY5
        p1_color = pymlgame.GREEN if len(self.game.players) > 1 \
            else pymlgame.GREY5

        surface = pymlgame.Surface(
            self.game.screen.width, self.game.screen.height)
        # note(hrantzsch): this works for our default screen size only
        drawing.draw_p(surface, Point(0, 2), p0_color)
        drawing.draw_0(surface, Point(4, 2), p0_color)
        drawing.draw_p(surface, Point(10, 2), p1_color)
        drawing.draw_1(surface, Point(14, 2), p1_color)
        self.game.screen.blit(surface)


class StartingState(GameState):
    """
    In this state, the game renders only the players' paddles for a given
    amount of time.
    """

    def __init__(self, game):
        super(self.__class__, self).__init__(game)
        self.init_time = time.time()
        self.delay = 3  # seconds between inner state changes

    def _should_proceed(self):
        return time.time() - self.init_time > self.delay

    def update(self):
        if self._should_proceed():
            self.game.state = RunningState(self.game)

    def render(self):
        # maybe a fancy countdown animation at each tick?
        for paddle in self.game.players.values():
            self.game.screen.blit(paddle.surface, paddle.position)


class RunningState(GameState):

    def update(self):
        if self.game.ball.position.x <= 0 or \
           self.game.ball.position.x >= self.game.screen.width-1:
            self.game.state = GameOverState(self.game)
            return

        if any([p.check_collision(self.game.ball)
                for p in self.game.players.values()]):
            self.game.ball.reflect("x")
        # note: we can collide with the paddle AND collide with the ceiling
        if self.game.ball.position.y <= 0 or \
           self.game.ball.position.y >= self.game.screen.height-1:
            self.game.ball.reflect("y")

        self.game.ball.update()

    def render(self):
        """
        Send the current screen content to Mate Light.
        """
        for paddle in self.game.players.values():
            self.game.screen.blit(paddle.surface, paddle.position)

        self.game.screen.blit(self.game.ball.surface,
                              tuple(map(round, self.game.ball.position)))


class GameOverState(GameState):

    def update(self):
        self.game.init_ball()
        for p in self.game.players.values():
            p.reset()
        self.game.state = StartingState(self.game)

    def render(self):
        # maybe a fancy highscore screen of some kind?
        pass
