#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymlgame
import random

from ball import Ball
from misc import Point
from paddle import Paddle
from game_states import WaitingState


class Game(object):
    """
    The main game class that holds the gameloop.
    """

    def __init__(self, mlhost, mlport, screen_width, screen_height):
        """
        Create a screen and define some game specific things.
        """
        pymlgame.init()
        self.screen = pymlgame.Screen(
            mlhost, mlport, screen_width, screen_height)
        self.clock = pymlgame.Clock(15)
        self.gameover = False
        self.players = {}
        self.state = WaitingState(self)
        self.init_ball()

    def init_ball(self):
        ball_position = Point(self.screen.width // 2, self.screen.height // 2)
        ball_velocity = Point(random.choice(
            [-1, 1]) * 0.5, random.choice([-1, 1]) * 0.2)
        self.ball = Ball(ball_position, ball_velocity)

    def construct_player(self, uid):
        self.players[uid] = Paddle(
            uid,
            self.screen,
            is_first_player=len(self.players) == 0
        )
        print('new ctlr with uid:', uid)

    def handle_events(self):
        """
        Loop through all events.
        """
        for event in pymlgame.get_events():
            if event.type == pymlgame.E_NEWCTLR:
                if len(self.players) < 2:
                    self.construct_player(event.uid)

            elif event.type == pymlgame.E_KEYDOWN or \
                    event.type == pymlgame.E_KEYPRESSED:
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
                self.screen.reset()
                self.state.update()
                self.state.render()
                self.screen.update()
                self.clock.tick()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Play Snake on your Matelight")
    parser.add_argument('host', help='remote host to connect to')
    parser.add_argument('-p', '--port', type=int,
                        default=1337, help='remote port')
    parser.add_argument('--width', type=int, default=15,
                        help='width of matelight')
    parser.add_argument('--height', type=int, default=16,
                        help='height of matelight')
    parser.add_argument('--demo', action='store_true',
                        default=False, help='start game in demo mode')

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
