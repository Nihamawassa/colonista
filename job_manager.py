'''
Created on 08.12.2012

@author: JR
'''


class JobManager(object):
    
    colonistlist = []
    
    def __init__(self, cl):
        self.colonistlist = cl

    def update_jobmanager(self, cl):
        self.colonistlist = cl


class Job(object):

    def __init__(self, name):
        self.name = "Idle"
        self.worker

    def update_job(self):
        pass


class FarmWork(Job):

    name = "farmwork"

    def __init__(self):
        Job.__init__(self, self.name)

    def update_job(self):
        Job.update_job(self)