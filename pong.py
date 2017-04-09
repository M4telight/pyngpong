#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import pymlgame
import random
import time

from ball import Ball
from misc import Point
from paddle import Paddle

import drawing

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
        self.state = "WAITING_FOR_PLAYERS"
        self.init_ball()

    def init_ball(self):
        ball_position = Point(self.screen.width // 2, self.screen.height // 2)
        ball_velocity = Point(random.choice([-1, 1]) * 0.5, random.choice([-1, 1]) * 0.2)
        self.ball = Ball(ball_position, ball_velocity)

    def update_and_render(self):
        self.screen.reset()

        if self.state == "WAITING_FOR_PLAYERS":
            self.update_waiting()
            self.render_waiting()
        elif self.state == "START_GAME":
            self.update_start_game()
        elif self.state == "RUNNING":
            self.update_running()
            self.render_running()
        elif self.state == "GAME_OVER":
            self.update_game_over()
        else:
            print("That's simply poor programming...")

        self.screen.update()
        self.clock.tick()

    def update_waiting(self):
        if len(self.players) == 2:
            self.state = "START_GAME"

    def render_waiting(self):
        p0_color = pymlgame.GREY5
        p1_color = pymlgame.GREY5
        if len(self.players) > 0:
            p0_color = pymlgame.GREEN
        if len(self.players) > 1:
            p1_color = pymlgame.GREEN

        surface = pymlgame.Surface(self.screen.width, self.screen.height)
        # note(hrantzsch): this works for our default screen size only
        drawing.draw_p(surface, Point(0, 2), p0_color)
        drawing.draw_0(surface, Point(4, 2), p0_color)
        drawing.draw_p(surface, Point(10, 2), p1_color)
        drawing.draw_1(surface, Point(14, 2), p1_color)
        self.screen.blit(surface)

    def update_start_game(self):
        time.sleep(2)
        self.state = "RUNNING"

    def update_running(self):
        if any([p.check_collision(self.ball) for p in self.players.values()]):
            self.ball.reflect("x")
        if self.ball.position.y <= 0 or \
           self.ball.position.y >= self.screen.height-1:
            self.ball.reflect("y")

        elif self.ball.position.x <= 0 or \
           self.ball.position.x >= self.screen.width-1:
            self.state = "GAME_OVER"
            # todo(hrantzsch): we don't want to update the ball here -- refactor
        self.ball.update()

    def render_running(self):
        """
        Send the current screen content to Mate Light.
        """
        for paddle in self.players.values():
            self.screen.blit(paddle.surface, paddle.position)

        self.screen.blit(self.ball.surface,
                         tuple(map(round, self.ball.position)))

    def update_game_over(self):
        self.init_ball()
        for p in self.players.values():
            p.reset()
        self.state = "START_GAME"

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

            elif event.type == pymlgame.E_KEYDOWN or event.type == pymlgame.E_KEYPRESSED:
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
                self.update_and_render()
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
        GAME.state = "START_GAME"

    GAME.gameloop()
