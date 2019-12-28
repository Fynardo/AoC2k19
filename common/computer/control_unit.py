class ControlUnit:
    halt_code = 99
    def __init__(self, iosystem):
        self.pc = 0 # Program counter
        self.base_register = 0 # Relative addresing register
        self.iosystem = iosystem 
        self._is_running = True

    def attach(self, scheduler_callback):
        self.notify = scheduler_callback

    def reset(self, intcode):
        self.restore(intcode, 0)

    def get_current_state(self):
        return self.intcode, self.pc

    def restore(self, intcode, pc):
        self.intcode = intcode
        self.pc = pc
        self._is_running = True
    
    def run(self):
        while self._is_running:           
            opcode = self._fetch_immediate()
            self._execute(opcode)
        return 0
            
    def _store_value(self, value, addr):
        self.intcode.write(value, addr)

    def _update_pc(self, addr):
        self.pc = addr

    def _fetch_position(self):
        val = self.intcode.read(self.pc)
        self.pc += 1
        return self.intcode.read(val)

    def _fetch_immediate(self):
        val = self.intcode.read(self.pc)
        self.pc += 1
        return val

    def _fetch_relative(self):
        offset = self.intcode.read(self.pc)
        self.pc += 1
        return self.intcode.read(self.base_register + offset)

    def _execute(self, opcode):
        instr_code = opcode % 100 # instruction codes use 2 digits
        opcode //= 100
        
        next_instr = self._instruction_builder(instr_code)
        next_instr(opcode)
        self.notify(instr_code)

    def _fetch_params(self, opcode, params_count):
        params = []
        for i in range(params_count):
            mode = opcode % 10            
            if mode == 0:
                params.append(self._fetch_position())
            if mode == 1:
                params.append(self._fetch_immediate())
            if mode == 2:
                params.append(self._fetch_relative())
            opcode //= 10
        return params

    def _fetch_resaddr(self, opcode):
        opcode //= 100
        mode = opcode % 10
        if mode == 0 or mode == 1:
            addr = self._fetch_immediate()
        elif mode == 2:
            offset = self.intcode.read(self.pc)        
            self.pc += 1
            addr = self.base_register + offset
        return addr

    def _add(self, opcode):
        op1, op2 = self._fetch_params(opcode, 2)       
        addr = self._fetch_resaddr(opcode)        
        self._store_value(op1+op2, addr)

    def _multiply(self, opcode):
        op1, op2 = self._fetch_params(opcode, 2)
        addr = self._fetch_resaddr(opcode)
        self._store_value(op1*op2, addr)

    def _input(self, opcode):
        val = self.iosystem.read()
        addr = self._fetch_resaddr(opcode*100)
        self._store_value(val, addr)

    def _output(self, opcode):
        op1 = self._fetch_params(opcode, 1)[0]
        self.iosystem.write(op1)        

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
        addr = self._fetch_resaddr(opcode)
        self._store_value(1 if op1 < op2 else 0, addr)

    def _equals(self, opcode):
        op1, op2 = self._fetch_params(opcode, 2)
        addr = self._fetch_resaddr(opcode)
        self._store_value(1 if op1 == op2 else 0, addr)

    def _adjust_relative_base(self, opcode):
        offset = self._fetch_params(opcode, 1)[0]
        self.base_register += offset

    def _halt(self, opcode):
        self._is_running = False

    def _instruction_builder(self, code):
        builder = {1: self._add, 2: self._multiply, 3: self._input, 4: self._output, 5: self._jump_if_true, 6: self._jump_if_false, 7: self._less_than, 8: self._equals, 9: self._adjust_relative_base, 99: self._halt}
        return builder[code]

