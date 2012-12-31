'''
Created on 08.12.2012

@author: JR
'''


class JobManager(object):
    
    colonistlist = []
    workplacelist = []
    freeworkforce = []
    joblist = []
    
    def __init__(self, cl, wl):
        self.colonistlist = cl
        self.workplacelist = wl

    def update_jobmanager(self, cl, wl):
        self.colonistlist = cl
        self.workplacelist = wl
        for colonist in self.colonistlist:
            if colonist.job == "Unemployed":
                self.freeworkforce = self.freeworkforce[:] + [colonist.id]
        for workplace in self.workplacelist:
            if workplace.needed_workers != 0:
                self.joblist = self.joblist[:] + [Job(workplace.job_name, workplace.id)]
        if len(self.freeworkforce) < len(self.joblist):
            pass


class Job(object):

    def __init__(self, name, id):
        self.name = name
        self.workplace_id = id
        self.worker = 0

    def update_job(self):
        pass