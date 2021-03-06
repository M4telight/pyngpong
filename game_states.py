import pygame
import pymlgame
import time
import math

from misc import Point, PygameSurfaceDecorator


class GameState:
    """
    Abstract base class for a state of a pyngpong game. Derived classes should
    implement update() and render().
    States will go ahead and replace themselves by another state if they deem
    it necessary.
    """

    def __init__(self, game):
        self.game = game

    def _init_font_rendering(self):
        if not pygame.font.get_init():
            pygame.font.init()

        self.font = pygame.font.Font('assets/fonts/6px2bus.ttf', 6)

    def update(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError


class WaitingState(GameState):
    """
    In this state, the game waits for 2 players to join.
    """

    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
        self._init_font_rendering()

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
        player0 = PygameSurfaceDecorator(
            self.font.render("P0", False, p0_color, pymlgame.BLACK)
        )
        surface.blit(player0, Point(0, 2))

        player1 = PygameSurfaceDecorator(
            self.font.render("P1", False, p1_color, pymlgame.BLACK)
        )
        surface.blit(player1, Point(8, 2))

        self.game.screen.blit(surface)


class PauseState(GameState):
    """
    In this state, the game renders only the players' paddles for a given
    amount of time.
    """

    def __init__(self, game):
        super().__init__(game)
        self.init_time = time.time()

        self._init_font_rendering()

        self.screen_center = Point(
            math.ceil(self.game.screen.width / 2),
            self.game.screen.height // 2,
        )

    def _time_elapsed(self):
        return int(time.time() - self.init_time)

    def _should_proceed(self):
        return self._time_elapsed() > self.delay

    def update(self):
        self.game.init_ball()

        if self._should_proceed():
            self.game.state = self.next_state

    def render(self):
        # maybe a fancy countdown animation at each tick?
        for paddle in self.game.players.values():
            self.game.screen.blit(paddle.surface, paddle.position)


class StartingState(PauseState):
    """
    In this state, the game renders only the players' paddles for a given
    amount of time as well as a countdown.
    """

    def __init__(self, game):
        super().__init__(game)
        self.delay = 5  # seconds between inner state changes

        self.next_state = RunningState(self.game)

    def render(self):
        super().render()

        # get time we still have to wait and render it to center of screen
        text = str(self.delay - self._time_elapsed())
        time_left_surface = PygameSurfaceDecorator(
            self.font.render(text, False, pymlgame.DARKYELLOW, pymlgame.BLACK)
        )

        time_left_center = Point(
            time_left_surface.width // 2,
            time_left_surface.height // 2
        )
        self.game.screen.blit(
            time_left_surface,
            self.screen_center - time_left_center
        )


class ScoredState(PauseState):
    """
    In this state, the game renders only the players' paddles for a given
    amount of time as well as the score.
    """

    def __init__(self, game):
        super().__init__(game)

        self.delay = 3  # seconds between inner state changes

        self.next_state = RunningState(self.game)

    def render(self):
        super().render()

        # get score and render it to center of screen
        text = ':'.join(map(str, self.game.scores.values()))
        time_left_surface = PygameSurfaceDecorator(
            self.font.render(text, False, pymlgame.DARKYELLOW, pymlgame.BLACK)
        )

        time_left_center = Point(
            time_left_surface.width // 2,
            time_left_surface.height // 2
        )
        self.game.screen.blit(
            time_left_surface,
            self.screen_center - time_left_center
        )



class RunningState(GameState):

    def __init__(self, game):
        super().__init__(game)

    def _check_if_scored(self):
        if self.game.ball.position.x <= 0:
            uid = [p for p in self.game.players.values() if not p.is_first_player][0].player_id
            self.game.scores[uid] += 1
        elif self.game.ball.position.x >= self.game.screen.width - 1:
            uid = [p for p in self.game.players.values() if p.is_first_player][0].player_id
            self.game.scores[uid] += 1

    def update(self):
        self._check_if_scored()

        if self.game.ball.position.x <= 0 or \
         self.game.ball.position.x >= self.game.screen.width - 1:
            if any([s > 2 for s in self.game.scores.values()]):
                self.game.state = GameOverState(self.game)
                return
            else:
                self.game.state = ScoredState(self.game)
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
        for p in self.game.scores.keys():
            self.game.scores[p] = 0
        self.game.state = StartingState(self.game)

    def render(self):
        # maybe a fancy highscore screen of some kind?
        pass
