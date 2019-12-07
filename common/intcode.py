from abc import abstractmethod
import copy


class Intcode:
    @abstractmethod
    def restore(self):
        pass

    @abstractmethod
    def read(self, addr):
        pass        

    @abstractmethod
    def write(self, addr, value):
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
    
    def read(self, addr):
        return self._program[addr]

    def write(self, value, addr):
        self._program[addr] = value

    def get_result(self):
        return self._program[0]

