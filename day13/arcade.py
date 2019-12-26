# Day 13. Care Package

import sys
sys.path.append("..")
import common.intcode as intcode
import common.control_unit as control_unit
import common.iosystem as iosystem
import common.scheduler as scheduler

from dataclasses import dataclass
import random


tiles = [' ', '#', 'x', '|', 'o']
grid = {}


@dataclass
class DrawInstruction:
    x : int
    y : int
    tile : int


class Grid:
    def __init__(self):
        self._grid = {}
        self.score = -1
    
    def set_tile(self, instruction: DrawInstruction):       
        #print(instruction.x, instruction.y, instruction.tile)
        if instruction.x == -1 and instruction.y == 0:
            self.update_score(instruction.tile)            
        else:
            if instruction.x in self._grid:                
                self._grid[instruction.x][instruction.y] = tiles[instruction.tile]
            else:
                self._grid[instruction.x] = {instruction.y: tiles[instruction.tile]}

    def count_tiles(self, tile_id):
        to_count = [tile == tiles[tile_id] for rows, columns in self._grid.items() for column, tile in columns.items()]
        return sum(to_count)

    def update_score(self, value):
        self.score = value

    def get_score(self):
        return self.score

    def _track(self, tile):
        for x, cols in self._grid.items():
            for y, t in cols.items():
                if tile == t:
                    return x,y
        return None

    def track_ball(self):
        return self._track('o')

    def track_paddle(self):
        return self._track('|')

    def draw(self):
        x = self._grid.keys()
        #print(x)
        for x, cols in self._grid.items():
            row = ''
            for y, tile in cols.items():
                row += tile
            print(row)
        print('CURRENT SCORE: {}'.format(self.get_score()))

    
class Controller(scheduler.SingleProgram):
    def __init__(self, control_unit, io, grid):
        super().__init__(control_unit)
        self.io = io
        self.grid = grid
        self.fsm = 0
        self.decoding_instruction = DrawInstruction(0,0,0)

    def _attached_unit_callback(self, instr):
        if instr == 4:
            if self.fsm == 0:
                self.decoding_instruction.x = io.read()
            elif self.fsm == 1:
                self.decoding_instruction.y = io.read()
            elif self.fsm == 2:
                self.decoding_instruction.tile = io.read()
                self.grid.set_tile(self.decoding_instruction)               
            self.fsm = (self.fsm + 1) % 3
            

with open('input','r') as f:
    game_code = list(eval(f.read()))

grid = Grid()
io = iosystem.MemIOSystem()
cpu = control_unit.ControlUnit(io)
controller = Controller(cpu, io, grid)
arcade_cabinet = scheduler.Job('Arcade Game', intcode.ListIntcode(game_code+([0]*16000)), 0)
controller.add_job(arcade_cabinet)
controller.run()


print('Part One. Drawing Tiles...')
print('Done! {} Block tiles shown on screen'.format(grid.count_tiles(2)))

input('Press any key to let the computer play the game!')


# Part Two
def move_paddle():
    ball = grid.track_ball()
    paddle = grid.track_paddle()
    #print('BALL IS IN {}'.format(ball))
    #print('PADDLE IS IN {}'.format(paddle))
    move = 0
    if ball[0] > paddle[0]:
        move = 1
    elif ball[0] == paddle[0]:
        move = 0
    elif ball[0] < paddle[0]:
        move = -1 
    return move


def move_joystick():
    #grid.draw() # Uncomment to see the game screen (kinda rotated btw)
    move = move_paddle()
    #print('Moving joystick to: {}'.format(move))
    return move


class Joystick(scheduler.SingleProgram):
    def __init__(self, control_unit, io, grid):
        super().__init__(control_unit)
        self.io = io
        self.grid = grid
        self.fsm = 0        
        self.decoding_instruction = DrawInstruction(0,0,0)        

    def _attached_unit_callback(self, instr):
        if instr == 4:
            #print('Instruction: {}'.format(instr))  
            #print(self.io._buffer)
            if self.fsm == 0:                    
                self.decoding_instruction.x = io.async_read()
            elif self.fsm == 1:
                self.decoding_instruction.y = io.async_read()
            elif self.fsm == 2:
                self.decoding_instruction.tile = io.async_read()
                self.grid.set_tile(self.decoding_instruction)                      
            self.fsm = (self.fsm + 1) % 3

       
with open('input','r') as f:
    game_code = list(eval(f.read()))

game_code[0] = 2

grid = Grid()
io = iosystem.SyncMemIOSystem(move_joystick)
cpu = control_unit.ControlUnit(io)
joystick = Joystick(cpu, io, grid)
arcade_cabinet = scheduler.Job('Arcade Game', intcode.ListIntcode(game_code+([0]*16000)), 0)
joystick.add_job(arcade_cabinet)
joystick.run()

print('\n\nWINNER! FINAL SCORE: {}'.format(grid.get_score()))










