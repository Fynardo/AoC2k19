# Advent of Code day 5. Sunny with a chance of asteroids
import sys
sys.path.append("..")
import common.intcode as intcode
import common.computer as computer
  

# Part One
print('Part One: To Test Air conditioner system (1):')

assist = intcode.ListIntcode()
assist.load('input')
assist_computer = computer.Computer(assist)
final_state = assist_computer.run()


# Part Two
print('Part Two: Fixing Thermal radiators (5):')
assist = intcode.ListIntcode()
assist.load('input')
assist_computer = computer.Computer(assist)
final_state = assist_computer.run()

