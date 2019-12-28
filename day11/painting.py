# Day 11: Space Police

import sys
sys.path.append("..")
import common.computer.intcode as intcode
import common.computer.control_unit as control_unit
import common.computer.iosystem as iosystem
import common.computer.scheduler as scheduler



"""
    HullMap utilities
"""

color_to_binary = {'.':0, '#':1}
binary_to_color = ['.','#']

class HullMap:
    def __init__(self):
        self.panels = {}

    def paint(self, color, location):
        self.panels[location] = color

    def read_panel(self, location):
        return self.panels[location] if location in self.panels else '.'


""" 
    Robot Logic is implemented with a state pattern that handles the current direction the robot is facing and how it should advance through the hull
"""
class FacingUp:
    facing = '^'

    @staticmethod
    def turn_right():
        return FacingRight

    @staticmethod
    def turn_left():
        return FacingLeft

    @staticmethod
    def advance(current_loc):
        current_x = current_loc[0]
        current_y = current_loc[1]
        return (current_x, current_y-1)


class FacingRight:
    facing = '>'

    @staticmethod
    def turn_right():
        return FacingDown

    @staticmethod
    def turn_left():
        return FacingUp

    @staticmethod
    def advance(current_loc):
        current_x = current_loc[0]
        current_y = current_loc[1]
        return (current_x+1, current_y)

class FacingDown:
    facing = 'v'

    @staticmethod
    def turn_right():
        return FacingLeft

    @staticmethod
    def turn_left():
        return FacingRight

    @staticmethod
    def advance(current_loc):
        current_x = current_loc[0]
        current_y = current_loc[1]
        return (current_x, current_y+1)
    
    
class FacingLeft:
    facing = '<'

    @staticmethod
    def turn_right():
        return FacingUp

    @staticmethod
    def turn_left():
        return FacingDown

    @staticmethod
    def advance(current_loc):
        current_x = current_loc[0]
        current_y = current_loc[1]
        return (current_x-1, current_y)


class Robot:
    def __init__(self, hull_map):
        self.hull_map = hull_map
        self.state = FacingUp
        self.location = (0,0)

    def paint(self, color):
        self.hull_map.paint(color, self.location)

    def read_panel(self):
        return self.hull_map.read_panel(self.location)        

    def turn_right(self):
        self.state = self.state.turn_right()

    def turn_left(self):
        self.state = self.state.turn_left()

    def advance(self):
        self.location = self.state.advance(self.location)

    def __str__(self):
        return '{}: {}'.format(self.state.facing, self.location)


class Controller(scheduler.SingleProgram):
    """
        Robot Camera Controller: Inputs the color of the pane and tracks for output calls to move the robot around and track how the panels are painted
    """
    def __init__(self, control_unit, iosystem, robot, starting_panel):
        super().__init__(control_unit)
        self.io = iosystem
        self.robot = robot
        self.fsm = True # Kinda Stupid Finite State Machine to track when to paint (True) and when to rotate (False)

        self.io.write(color_to_binary[starting_panel]) # Initialize robot

    def _attached_unit_callback(self, instr):
        if instr == 4:
            cmd = self.io.read()                        
            if self.fsm:
                self.robot.paint(binary_to_color[cmd])                
            else:
                if cmd == 0:
                    self.robot.turn_left()
                elif cmd == 1:
                    self.robot.turn_right()
                self.robot.advance()
                self.io.write(color_to_binary[self.robot.read_panel()])
            self.fsm = not self.fsm


# Part One
with open('input','r') as f:
    paint_code = list(eval(f.read()))


hull_map = HullMap()
painting_robot = Robot(hull_map)

io = iosystem.MemIOSystem()
robot_cpu = control_unit.ControlUnit(io)
controller = Controller(robot_cpu, io, painting_robot, '.')
paint_program = scheduler.Job('HULL PAINTING', intcode.ListIntcode(paint_code+([0]*16000)), 0)
controller.add_job(paint_program)
controller.run()

print('Part One. Printing the hull...')
print('Done! Printed {} panels at least once'.format(len(hull_map.panels.keys())))


# Part Two
hull_map = HullMap()
painting_robot = Robot(hull_map)

io = iosystem.MemIOSystem()
robot_cpu = control_unit.ControlUnit(io)
controller = Controller(robot_cpu, io, painting_robot, '#')
paint_program = scheduler.Job('HULL PAINTING', intcode.ListIntcode(paint_code+([0]*16000)), 0)
controller.add_job(paint_program)
controller.run()


def calculate_hull_limits(hull_map, axis):
    k = hull_map.panels.keys()
    return min(k, key= lambda x: x[axis])[axis], max(k, key= lambda x: x[axis])[axis]
        

xlim = calculate_hull_limits(hull_map, 0)
ylim = calculate_hull_limits(hull_map, 1)    

print('\nPart Two. Reading registration identifier')
for i in range(*ylim):
    row = ''
    for j in range(*xlim):
         row += hull_map.read_panel((j,i))
    print(row)







