# Advent of Code day 2. 1202 Program Alarm
import sys
sys.path.append("..")
import common.computer.intcode as intcode
import common.computer.control_unit as control_unit
import common.computer.iosystem as iosystem
import common.computer.scheduler as scheduler

  

# Part One
# Tests
print('Part One. Testing')
programs = [[1,0,0,0,99], [2,3,0,3,99], [2,4,4,5,99,0], [1,1,1,4,99,5,6,0,99] ]
for i, program in enumerate(programs):
    io = iosystem.StdIOSystem()
    ship_processor = control_unit.ControlUnit(io)
    sched = scheduler.SingleProgram(ship_processor)
    code = intcode.ListIntcode(program)
    alarm_test = scheduler.Job('Alarm_Test',code , 0)
    sched.add_job(alarm_test)    
    sched.run()    
    print('Program #{} test: {} -> {} [{}]'.format(i, program, code._code, code._code[0]))


# Gravity assist program
with open('input','r') as f:
    program = list(eval(f.read()))

io = iosystem.StdIOSystem()
ship_processor = control_unit.ControlUnit(io)
sched = scheduler.SingleProgram(ship_processor)
assist_program = intcode.ListIntcode(program)
assist_program.restore(12,2)
alarm_fix = scheduler.Job('Alarm', assist_program, 0)
sched.add_job(alarm_fix)    
sched.run()  

print('Part 1: Running Gravity Assist: {}'.format(assist_program._code[0]))


# Part Two

def bruteforce():
    for noun in range(100):
        for verb in range(100):
            io = iosystem.StdIOSystem()
            ship_processor = control_unit.ControlUnit(io)
            sched = scheduler.SingleProgram(ship_processor)
            assist_program = intcode.ListIntcode(program)
            assist_program.restore(noun,verb)
            alarm_fix = scheduler.Job('Alarm', assist_program, 0)
            sched.add_job(alarm_fix)    
            sched.run() 
            
            if assist_program._code[0] == 19690720:
                print('Found!: {},{} -> {}'.format(noun, verb, 100*noun + verb))
                return noun, verb
print('Part 2: Getting that error code by bruteforce...')    
noun, verb = bruteforce()



