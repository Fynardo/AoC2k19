# -*- coding: utf-8 -*-
# Day 13. Care Package

import sys
sys.path.append("..")
import common.computer.intcode as intcode
import common.computer.control_unit as control_unit
import common.computer.iosystem as iosystem
import common.computer.scheduler as scheduler
from common.display.screen import Screen

from dataclasses import dataclass
import os
from abc import abstractmethod


@dataclass
class DrawInstruction:
    x : int
    y : int
    tile : int


class GamePlay(scheduler.SingleProgram):
    def __init__(self, control_unit, io, screen_driver, player):
        super().__init__(control_unit)
        self.io = io
        self.fsm = 0
        self.decoding_instruction = DrawInstruction(0, 0, 0)

        self.screen_driver = screen_driver
        self.player = player
        self.score = 0

    def _attached_unit_callback(self, instr):
        if instr == 4:
            if self.fsm == 0:
                self.decoding_instruction.x = io.async_read()
            elif self.fsm == 1:
                self.decoding_instruction.y = io.async_read()
            elif self.fsm == 2:
                self.decoding_instruction.tile = io.async_read()
                if self.decoding_instruction.x == -1 and self.decoding_instruction.y == 0:
                    self.update_score(self.decoding_instruction.tile)
                else:
                    self.screen_driver.set_tile(self.decoding_instruction.x, self.decoding_instruction.y, self.decoding_instruction.tile)
            self.fsm = (self.fsm + 1) % 3

    def update_score(self, value):
        self.score = value
        self.screen_driver.update_score(self.score)

    def get_score(self):
        return self.score


class ScreenDriver:
    def __init__(self, screen):
        self.tiles = [' ', '#', 'x', '_', 'o']
        self.screen = screen

    def draw(self):
        self.screen.draw()

    def get_screen_size(self):
        return self.screen.width, self.screen.height

    def set_tile(self, x, y, tile):
        self.screen.set_tile(y, x, self.tiles[tile])

    def get_tile(self, x, y):
        return self.screen.get_tile(x, y)

    def update_score(self, score):
        self.screen.set_text(self.screen.height-1, 0, 'SCORE: '+str(score))


class Player:
    def  __init__(self, screen_driver):
        self.screen_driver = screen_driver

    def play(self):
        """
        Since all this architecture is kinda strange, I have to print here which is weird but it works.
        Also, clearing the screen and drawing in realtime it's kinda hipnotic. Not drawing anything should speed up
        the game as well.
        """
        os.system('clear')
        self.screen_driver.draw()
        next_move = self._make_move()
        return next_move

    @abstractmethod
    def _make_move(self):
        pass

class IAPlayer(Player):
    def _make_move(self):
        ball = self._track_ball()
        paddle = self._track_paddle()
        move = 0
        if ball[0] > paddle[0]:
            move = 1
        elif ball[0] == paddle[0]:
            move = 0
        elif ball[0] < paddle[0]:
            move = -1
        return move

    def _track_tile(self, tile):
        w, h = self.screen_driver.get_screen_size()
        for i in range(h):
            for j in range(w):
                if self.screen_driver.get_tile(i, j) == tile:
                    return j,i

    def _track_paddle(self):
        return self._track_tile('_')

    def _track_ball(self):
        return self._track_tile('o')


class HumanPlayer(Player):
    def _make_move(self):
        move = int(input('Move: '))
        return move


# Part One
def count_blocks(screen_driver):
    block_tile = 'x'
    count = 0
    w, h = screen_driver.get_screen_size()
    for i in range(h):
        for j in range(w):
            if screen_driver.get_tile(i, j) == block_tile:
                count += 1
    return count

with open('input','r') as f:
    game_code = list(eval(f.read()))

screen = Screen()
screen_driver = ScreenDriver(screen)
player = IAPlayer(screen_driver)
io = iosystem.SyncMemIOSystem(player.play)
cpu = control_unit.ControlUnit(io)
cabinet = GamePlay(cpu, io, screen_driver, player)
game = scheduler.Job('Arcade Game', intcode.ListIntcode(game_code+([0]*16000)), 0)
cabinet.add_job(game)
cabinet.run()

print('Part One. Drawing Tiles...')
print('Done! {} Block tiles shown on screen'.format(count_blocks(screen_driver)))


# Part Two
input('\nPart Two. Starting Game, press any key to continue')

with open('input','r') as f:
    game_code = list(eval(f.read()))

game_code[0] = 2 # Insert those coins

screen = Screen()
screen_driver = ScreenDriver(screen)
player = IAPlayer(screen_driver)
io = iosystem.SyncMemIOSystem(player.play)
cpu = control_unit.ControlUnit(io)
cabinet = GamePlay(cpu, io, screen_driver, player)
game = scheduler.Job('Arcade Game', intcode.ListIntcode(game_code+([0]*16000)), 0)
cabinet.add_job(game)
cabinet.run()

screen_driver.draw()
