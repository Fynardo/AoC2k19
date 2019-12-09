from abc import abstractmethod

class IOSystem:
    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, value):
        pass


class StdIOSystem(IOSystem):
    def read(self):
        value = int(input('Enter input value: '))
        return value
    
    def write(self, value):
        print('Program Output: {}'.format(value))


class MemIOSystem(IOSystem):
    def __init__(self):
        self._buffer = [] # Stackl
   
    def read(self):
        if self._buffer:
            return self._buffer.pop(0)
        else:
            return None

    def write(self, value):
        self._buffer.append(value)
        
    def insert(self, pos, value):
        self._buffer.insert(pos, value)
