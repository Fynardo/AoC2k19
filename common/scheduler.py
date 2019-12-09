from abc import abstractmethod


class Job:
    """ Utility Class to track jobs (intcode programs) to schedule and execute"""
    def __init__(self, uuid, code, pc):
        self.uuid = uuid
        self.code = code
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

    @abstractmethod
    def _get_next_job(self):
        pass

    @abstractmethod
    def run(self):
        pass

    def _attached_unit_callback(self, instr):
        pass




    


        
