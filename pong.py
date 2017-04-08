#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import pymlgame

from misc import Point
from paddle import Paddle

class Game(object):
    """
    The main game class that holds the gameloop.
    """
    def __init__(self, mlhost, mlport, screen_width, screen_height):
        """
        Create a screen and define some game specific things.
        """
        pymlgame.init()
        self.screen = pymlgame.Screen(mlhost, mlport, screen_width, screen_height)
        self.clock = pymlgame.Clock(15)
        self.gameover = False

        self.init_paddles()
        self.init_ball()

    def init_paddles(self):
        self.paddles = []
        self.paddles.append(Paddle(1, self.screen))
        self.paddles.append(Paddle(2, self.screen, is_first_player=False))

    def init_ball(self):
        self.ball_surface = pymlgame.Surface(1, 1)
        self.ball_surface.draw_dot((0, 0), pymlgame.GREEN)

    def update(self):
        """
        Update the screens contents in every loop.
        """
        pass

    def render(self):
        """
        Send the current screen content to Mate Light.
        """
        self.screen.reset()

        self.screen.blit(self.ball_surface, (10, 10))
        for paddle in self.paddles:
            self.screen.blit(paddle.surface, paddle.position)

        self.screen.update()
        self.clock.tick()

    def handle_events(self):
        """
        Loop through all events.
        """
        pass

    def gameloop(self):
        """
        A game loop that circles through the methods.
        """
        try:
            while not self.gameover:
                self.handle_events()
                self.update()
                self.render()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Play Snake on your Matelight")
    parser.add_argument('host', help='remote host to connect to')
    parser.add_argument('-p', '--port', type=int, default=1337, help='remote port')
    parser.add_argument('--width', type=int, default=15, help='width of matelight')
    parser.add_argument('--height', type=int, default=16, help='height of matelight')

    args = parser.parse_args()
    GAME = Game(
        args.host,
        args.port,
        args.width,
        args.height,
    )
    GAME.gameloop()
