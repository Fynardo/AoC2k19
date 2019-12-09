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


# Part One
class FCFS(scheduler.Scheduler):
    """ Day 7.1 Scheduler. Jobs are executed until halt. """
    def __init__(self, control_unit, iosystem, phase_settings):
        super().__init__(control_unit)
        self.iosystem = iosystem
        self._phase_settings = phase_settings
        self._phase_idx = 0

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
        while self._pending_jobs:
            
            job = self._get_next_job() 
            self._running_job = job            

            # Trick to get phase and input signal to the control_unit (I don't have any proper memory system yet)            
            self._feed_job_params(input_signal)
                     
            self._control_unit.restore(job.code, job.pc)
            self._control_unit.run()

            input_signal = self.iosystem.read()


        self.iosystem.write(input_signal)
        return 0



# I'm creating a new environment for each execution
phase_values = [0,1,2,3,4]
def create_scheduler(code, phase_settings):
    io = iosystem.MemIOSystem()
    ship_processor = control_unit.ControlUnit(io)
    sched = FCFS(ship_processor, io, phase_settings)

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
test_programs = [[3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0],
[3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0],
[3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]]

test_signals = [43210, 54321, 65210]
test_sequences = [[4,3,2,1,0], [0,1,2,3,4], [1,0,4,3,2]]

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









