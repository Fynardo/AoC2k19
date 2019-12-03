# Advent of Code day 2. 1202 Program Alarm

from abc import abstractmethod
import copy

class Intcode:
    @abstractmethod
    def restore(self):
        pass

    @abstractmethod
    def read(self, address):
        pass        

    @abstractmethod
    def write(self, address, value):
        pass

    @abstractmethod
    def get_result(self):
        pass


class ListIntcode(Intcode):
    def __init__(self, program=None):
        self._program = copy.copy(program)

    def restore(self, noun, verb):
        self._program[1] = noun
        self._program[2] = verb

    def load(self, path):       
        with open(path, 'r') as f:
            self._program = list(eval(f.read()))      
    
    def read(self, address):
        return self._program[address]

    def write(self, address, value):
        self._program[address] = value

    def get_result(self):
        return self._program[0]


class Computer:
    halt_code = 99
    def __init__(self, intcode):
        self.intcode = intcode

    def run(self):
        pc = 0 # Program counter
        opcode = self.fetch(pc)
        while opcode != Computer.halt_code:           
            op1, op2, resdir = self.decode(pc)
            self.execute(opcode, op1, op2, resdir)
            pc += 4
            opcode = self.fetch(pc)
        return self.intcode
            
    def fetch(self, pc):
        return self.intcode.read(pc)

    def decode(self, pc):
        return self.intcode.read(pc+1), self.intcode.read(pc+2), self.intcode.read(pc+3)

    def execute(self, opcode, op1, op2, resdir):
        op = self._op_builder(opcode)
        op(op1, op2, resdir)
        
    def _add(self, op1, op2, resdir):
        self.intcode.write(resdir, self.intcode.read(op1) + self.intcode.read(op2))

    def _multiply(self, op1, op2, resdir):
        self.intcode.write(resdir, self.intcode.read(op1) * self.intcode.read(op2))

    def _op_builder(self, opcode):
        op_dict = {1: self._add, 2: self._multiply}
        return op_dict[opcode]
    

# Part One
# Tests
print('Executing tests')
programs = [[1,0,0,0,99], [2,3,0,3,99], [2,4,4,5,99,0], [1,1,1,4,99,5,6,0,99] ]
for i, program in enumerate(programs):
    intcode = ListIntcode(program)
    my_computer = Computer(intcode)
    final_state = my_computer.run()    
    print('Program #{} test: {} -> {} [{}]'.format(i, program, final_state._program, final_state.get_result()))

# Gravity assist program
assist = ListIntcode()
assist.load('input')
assist.restore(12, 2)
assist_computer = Computer(assist)
final_state = assist_computer.run()
print('Part 1: Running Gravity Assist: {}'.format(final_state.get_result()))


# Part Two
def bruteforce():
    for noun in range(100):
        for verb in range(100):
            assist = ListIntcode()
            assist.load('input')
            assist.restore(noun, verb)
            assist_computer = Computer(assist)
            final_state = assist_computer.run()
            if final_state.get_result() == 19690720:
                print('Found!: {},{}'.format(noun, verb))
                return noun, verb
    
noun, verb = bruteforce()
print('Part 2: Getting that error code {}'.format(100*noun + verb))




