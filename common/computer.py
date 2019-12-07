class Computer:
    halt_code = 99
    def __init__(self, intcode):
        self.intcode = intcode
        self.pc = 0 # Program counter

    def run(self):
        opcode = self._fetch_immediate()
        while opcode != Computer.halt_code:
            self._execute(opcode)      
            opcode = self._fetch_immediate()
        return self.intcode
            
    def _store_value(self, value, addr):
        self.intcode.write(value, addr)

    def _update_pc(self, addr):
        self.pc = addr

    def _fetch_immediate(self):
        val = self.intcode.read(self.pc)
        self.pc += 1
        return val

    def _fetch_position(self):
        val = self.intcode.read(self.pc)
        self.pc += 1
        return self.intcode.read(val)

    def _execute(self, opcode):
        instr_code = opcode % 100 # instruction codes use 2 digits
        opcode //= 100
        
        next_instr = self._instruction_builder(instr_code)
        next_instr(opcode)        

    def _fetch_params(self, opcode, params_count):
        params = []
        for i in range(params_count):
            mode = opcode % 10            
            if mode == 0:
                params.append(self._fetch_position())
            if mode == 1:
                params.append(self._fetch_immediate())
            opcode //= 10
        return params

    def _add(self, opcode):
        op1, op2 = self._fetch_params(opcode, 2)
        resaddr = self._fetch_immediate()
        self._store_value(op1+op2, resaddr)

    def _multiply(self, opcode):
        op1, op2 = self._fetch_params(opcode, 2)
        resaddr = self._fetch_immediate()
        self._store_value(op1*op2, resaddr)

    def _input(self, opcode):
        addr = self._fetch_immediate()
        val = int(input('Enter ID of the system to test: '))
        self._store_value(val, addr)

    def _output(self, opcode):
        op1 = self._fetch_params(opcode, 1)[0]
        print('Test Output: {}'.format(op1))

    def _jump_if_true(self, opcode):
        op1, op2 = self._fetch_params(opcode, 2)
        if op1 != 0:
            self._update_pc(op2)
    
    def _jump_if_false(self, opcode):
        op1, op2 = self._fetch_params(opcode, 2)
        if op1 == 0:
            self._update_pc(op2)

    def _less_than(self, opcode):
        op1, op2 = self._fetch_params(opcode, 2)
        addr = self._fetch_immediate()
        self._store_value(1 if op1 < op2 else 0, addr)

    def _equals(self, opcode):
        op1, op2 = self._fetch_params(opcode, 2)
        addr = self._fetch_immediate()
        self._store_value(1 if op1 == op2 else 0, addr)

    def _instruction_builder(self, code):
        builder = {1: self._add, 2: self._multiply, 3: self._input, 4: self._output, 5: self._jump_if_true, 6: self._jump_if_false, 7: self._less_than, 8: self._equals}
        return builder[code]

