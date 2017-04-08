#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import pymlgame

from ball import Ball
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
        self.players = {}
        self.init_ball()

    def init_ball(self):
        ball_position = Point(11, 5)
        ball_velocity = Point(0.8, 0.3)
        self.ball = Ball(ball_position, ball_velocity)
        self.ball_surface = pymlgame.Surface(1, 1)
        self.ball_surface.draw_dot((0, 0), pymlgame.GREEN)

    def update(self):
        """
        Update the screens contents in every loop.
        """
        if any([p.check_collision(self.ball) for p in self.players.values()]):
            self.ball.reflect("x")
        if self.ball.position.y <= 0 or \
           self.ball.position.y >= self.screen.height-1:
            self.ball.reflect("y")

        elif self.ball.position.x <= 0 or \
           self.ball.position.x >= self.screen.width-1:
           # gameover()
            self.ball.reflect("x")
        self.ball.update()

    def render(self):
        """
        Send the current screen content to Mate Light.
        """
        self.screen.reset()

        for paddle in self.players.values():
            self.screen.blit(paddle.surface, paddle.position)

        self.screen.blit(self.ball_surface,
                         tuple(map(round, self.ball.position)))

        self.screen.update()
        self.clock.tick()

    def start_game(self):
        pass

    def construct_player(self, uid):
        self.players[uid] = Paddle(
            uid,
            self.screen,
            is_first_player=len(self.players) == 0
        )
        print('new ctlr with uid:', uid)
        if len(self.players) == 2:
            self.start_game()

    def handle_events(self):
        """
        Loop through all events.
        """
        for event in pymlgame.get_events():
            if event.type == pymlgame.E_NEWCTLR:
                if len(self.players) < 2:
                    self.construct_player(event.uid)

            elif event.type == pymlgame.E_KEYDOWN:
                if event.button == pymlgame.CTLR_UP:
                    self.players[event.uid].move_up()
                elif event.button == pymlgame.CTLR_DOWN:
                    self.players[event.uid].move_down()

            elif event.type == pymlgame.E_PING:
                print('ping from', event.uid)

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
    parser.add_argument('--demo', action='store_true', default=False, help='start game in demo mode')

    args = parser.parse_args()
    GAME = Game(
        args.host,
        args.port,
        args.width,
        args.height,
    )

    if args.demo:
        GAME.construct_player(1)
        GAME.construct_player(2)

    GAME.gameloop()
