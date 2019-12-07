# Advent of Code day 2. 1202 Program Alarm
import sys
sys.path.append("..")
import common.intcode as intcode
import common.computer as computer
  

# Part One
# Tests
print('Executing tests')
programs = [[1,0,0,0,99], [2,3,0,3,99], [2,4,4,5,99,0], [1,1,1,4,99,5,6,0,99] ]
for i, program in enumerate(programs):
    my_intcode = intcode.ListIntcode(program)
    my_computer = computer.Computer(my_intcode)
    final_state = my_computer.run()    
    print('Program #{} test: {} -> {} [{}]'.format(i, program, final_state._program, final_state.get_result()))

# Gravity assist program
assist = intcode.ListIntcode()
assist.load('input')
assist.restore(12, 2)
assist_computer = computer.Computer(assist)
final_state = assist_computer.run()
print('Part 1: Running Gravity Assist: {}'.format(final_state.get_result()))


# Part Two
def bruteforce():
    for noun in range(100):
        for verb in range(100):
            assist = intcode.ListIntcode()
            assist.load('input')
            assist.restore(noun, verb)
            assist_computer = computer.Computer(assist)
            final_state = assist_computer.run()
            if final_state.get_result() == 19690720:
                print('Found!: {},{}'.format(noun, verb))
                return noun, verb
print("Part 2: Getting that error code by bruteforce...")    
noun, verb = bruteforce()
print('Part 2: {}'.format(100*noun + verb))




