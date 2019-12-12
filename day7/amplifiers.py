# Advent of Code day 7. Amplification Circuit
import sys
sys.path.append("..")
import copy
import common.intcode as intcode
import common.control_unit as control_unit
import common.iosystem as iosystem
import common.scheduler as scheduler


def permutations(values):
    """ Calculates all permutations given a list of values """
    if len(values) == 1:
        return [values]

    retval = []  
    for i in range(len(values)): 
       phase = values[i]
       remaining = values[:i] + values[i+1:]
       for p in permutations(remaining): 
           retval.append([phase] + p) 
    return retval


class Day7Scheduler(scheduler.Scheduler):
    """ Day 7 requires a tricky scheduler, since phase and signal must be feeded with IO system (there is no memory system implemented yet. 
    """
    def __init__(self, control_unit, iosystem, phase_settings, callback_instr_code):
        super().__init__(control_unit)
        self.iosystem = iosystem
        self._phase_settings = phase_settings
        self._phase_idx = 0
        self._callback_instr_code = callback_instr_code

    def _get_phase(self):
        if self._phase_idx < len(self._phase_settings):
            phase = self._phase_settings[self._phase_idx]
            self._phase_idx += 1        
            return phase
        else:
            return None

    def available_phases(self):
        return self._phase_idx < len(self._phase_settings)

    def _feed_job_params(self, input_signal):
        if self.available_phases():
            self.iosystem.write(self._get_phase())
        self.iosystem.write(input_signal)  

    def _get_next_job(self):
        return self._pending_jobs.pop(0)

    def run(self):
        input_signal = 0
        job = self._get_next_job() 
        self._running_job = job      
        self._feed_job_params(input_signal)
        self._control_unit.restore(job.program, job.pc)       
        self._control_unit.run()
               
        self.iosystem.write(input_signal)
        return 0

    def _attached_unit_callback(self, instr):
        if instr == self._callback_instr_code:
            #print('Replacing job: {}'.format(self._running_job.uuid))
            if self._pending_jobs:
                job = self._get_next_job()
                input_signal = self.iosystem.read()
                self._feed_job_params(input_signal)
                self._control_unit.restore(job.program, job.pc)
                self._running_job = job


#Part One: Testing
phase_values = [0,1,2,3,4]

test_programs = [[3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0],
[3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0],
[3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]]

test_signals = [43210, 54321, 65210]
test_sequences = [[4,3,2,1,0], [0,1,2,3,4], [1,0,4,3,2]]


# I'm creating a new environment for each test
def create_scheduler(code, phase_settings):
    io = iosystem.MemIOSystem()
    ship_processor = control_unit.ControlUnit(io)
    sched = Day7Scheduler(ship_processor, io, phase_settings, callback_instr_code=99)

    amp_a = scheduler.Job('amp_a', intcode.ListIntcode(code), 0)
    amp_b = scheduler.Job('amb_b', intcode.ListIntcode(code), 0)
    amp_c = scheduler.Job('amp_c', intcode.ListIntcode(code), 0)
    amp_d = scheduler.Job('amp_d', intcode.ListIntcode(code), 0)
    amp_e = scheduler.Job('amp_e', intcode.ListIntcode(code), 0)

    jobs = [amp_a, amp_b, amp_c, amp_d, amp_e]

    for job in jobs:
        sched.add_job(job)

    return sched


def calculate_largest_signal(program):
    phase_sequences = permutations(phase_values)

    best_sequence = None
    largest_signal = -1
    for sequence in phase_sequences:
        sched = create_scheduler(program, sequence)
        sched.run()
        signal = sched.iosystem.read()

        if signal >= largest_signal:
            largest_signal = signal
            best_sequence = sequence

    return largest_signal, best_sequence


print('Part One. Testing')
for i, test_program in enumerate(test_programs):
    
    largest_signal, best_sequence = calculate_largest_signal(test_program)
    print('Test #{} Result: {}, with sequence {}'.format(i, largest_signal, best_sequence))
    assert largest_signal == test_signals[i]
    assert best_sequence == test_sequences[i]


print('Part One. Amplifiers Signal')
with open('input', 'r') as f:
    program = list(eval(f.read()))

largest_signal, best_sequence = calculate_largest_signal(program)
print('Largest Signal obtained is {}. Settings: {}'.format(largest_signal, best_sequence))


# Part Two: Another Tricky Scheduler with context change anytime an amplifier executes an output instruction and phase feeding necessity.
class Day72Scheduler(Day7Scheduler):
    """ Day 7.2 Scheduler. Jobs are executed until an output instruction, then next amplifier is loaded until they all finish. """

    def _attached_unit_callback(self, instr):
        if instr == self._callback_instr_code:
            #print('Replacing job: {}'.format(self._running_job.uuid))
            icode, pc = self._control_unit.get_current_state()
            self._running_job.pc = pc
            self._pending_jobs.append(self._running_job)

            if self._pending_jobs:
                job = self._get_next_job()
                input_signal = self.iosystem.read()
                self._feed_job_params(input_signal)
                self._control_unit.restore(job.program, job.pc)
                self._running_job = job



# Part Two
print('\nPART Two. Testing')
phase_values = [5,6,7,8,9]

test_programs = [[3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5],
[3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]]

test_signals = [139629729, 18216]
test_sequences = [[9,8,7,6,5], [9,7,8,5,6]]


def create_scheduler(code, phase_settings):
    io = iosystem.MemIOSystem()
    ship_processor = control_unit.ControlUnit(io)
    sched = Day72Scheduler(ship_processor, io, phase_settings, callback_instr_code=4)

    amp_a = scheduler.Job('amp_a', intcode.ListIntcode(code), 0)
    amp_b = scheduler.Job('amb_b', intcode.ListIntcode(code), 0)
    amp_c = scheduler.Job('amp_c', intcode.ListIntcode(code), 0)
    amp_d = scheduler.Job('amp_d', intcode.ListIntcode(code), 0)
    amp_e = scheduler.Job('amp_e', intcode.ListIntcode(code), 0)

    jobs = [amp_a, amp_b, amp_c, amp_d, amp_e]

    for job in jobs:
        sched.add_job(job)

    return sched


def calculate_loop_signal(program):
    phase_sequences = permutations(phase_values)

    best_sequence = None
    largest_signal = -1
    for sequence in phase_sequences:
        sched = create_scheduler(program, sequence)
        sched.run()
        signal = sched.iosystem.read()

        if signal >= largest_signal:
            largest_signal = signal
            best_sequence = sequence

    return largest_signal, best_sequence


for i, test_program in enumerate(test_programs):  
    largest_signal, best_sequence = calculate_loop_signal(test_program)
    print('Test #{} Result: {}, with sequence {}'.format(i, largest_signal, best_sequence))
    assert largest_signal == test_signals[i]
    assert best_sequence == test_sequences[i]



with open('input', 'r') as f:
    program = list(eval(f.read()))

largest_signal, best_sequence = calculate_loop_signal(program)
print('Largest Signal obtained is {}. Settings: {}'.format(largest_signal, best_sequence))
        
            



















