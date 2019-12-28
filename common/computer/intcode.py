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
    def __init__(self, code=None):
        self._code = copy.copy(code)

    def restore(self, noun, verb):
        self._code[1] = noun
        self._code[2] = verb

    def load(self, path):       
        with open(path, 'r') as f:
            self._code = list(eval(f.read()))      
    
    def read(self, addr):
        return self._code[addr]

    def write(self, value, addr):
        self._code[addr] = value

    def get_result(self):
        return self._code[0]


