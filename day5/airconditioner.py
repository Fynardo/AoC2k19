# Advent of Code day 5. Sunny with a chance of asteroids
import sys
sys.path.append("..")
import copy
import common.computer.intcode as intcode
import common.computer.control_unit as control_unit
import common.computer.iosystem as iosystem
import common.computer.scheduler as scheduler
  


with open('input','r') as f:
    program = list(eval(f.read()))

io = iosystem.StdIOSystem()
ship_processor = control_unit.ControlUnit(io)
sched = scheduler.SingleProgram(ship_processor)

boost = scheduler.Job('TEST', intcode.ListIntcode(program), 0)

sched.add_job(boost)

print('Loading TEST program: Options\n- (1) Test air conditioner system.\n- (5) Fix thermal radiators')
sched.run()





