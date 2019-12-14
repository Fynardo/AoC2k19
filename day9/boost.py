# Advent of Code day 9. Boost Program
import sys
sys.path.append("..")
import common.intcode as intcode
import common.control_unit as control_unit
import common.iosystem as iosystem
import common.scheduler as scheduler


with open('input','r') as f:
    test = list(eval(f.read()))

print('Loading BOOST program. Press 1 for debug, 2 for calculate coordinates')
io = iosystem.StdIOSystem()
ship_processor = control_unit.ControlUnit(io)
sched = scheduler.SingleProgram(ship_processor)
boost = scheduler.Job('BOOST', intcode.ListIntcode(test+([0]*16000)), 0)
sched.add_job(boost)
sched.run()





