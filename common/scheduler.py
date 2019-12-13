from abc import abstractmethod


class Job:
    """ Utility Class to track jobs (intcode programs) to schedule and execute"""
    def __init__(self, uuid, program, pc):
        self.uuid = uuid
        self.program = program
        self.pc = pc


class Scheduler:
    def __init__(self, control_unit):
        self._created_jobs = 0
        self._pending_jobs = []
        self._running_job = None
        self._control_unit = control_unit
        self._control_unit.attach(self._attached_unit_callback)

    def add_job(self, in_job):
        self._pending_jobs.append(in_job)

    def _get_next_job(self):
        return self._pending_jobs.pop(0)

    @abstractmethod
    def run(self):
        pass

    def _attached_unit_callback(self, instr):
        pass


class SingleProgram(Scheduler):
    def __init__(self, control_unit):
        super().__init__(control_unit)      

    def run(self):
        job = self._get_next_job()
        self._running_job = job
        self._control_unit.restore(job.program, job.pc)
        self._control_unit.run()
        return 0

    


        
