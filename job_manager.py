'''
Created on 08.12.2012

@author: JR
'''

from operator import attrgetter


class JobManager(object):
    
    def __init__(self, cs, cl, wl):
        self.central_state = cs     # Central State object
        self.colonistlist = cl      # List of Colonist objects 
        self.workplacelist = wl     # List of Workplace objects
        self.freeworkforce = []     # List of colonist id integers
        self.joblist = []           # List of Job objects

    def update_jobmanager(self, cl, wl):
        self.colonistlist = cl
        self.workplacelist = wl
        
        # Create jobs from workplaces which need workers
        for colonist in self.colonistlist:
            if colonist.job == "Unemployed":
                if self.freeworkforce.count(colonist.id) == 0:  # append only, if colonist isn't already in list
                    self.freeworkforce.append(colonist.id)
        for workplace in self.workplacelist:
            if workplace.needed_workers > 0:
                # Repeat the following job creation for all needed workers
                for n in range(workplace.needed_workers):
                    i = 0
                    for job in self.joblist:
                        if job.workplace_id == workplace.id and job.worker == 0:
                            i =+ 1
                    if i < workplace.needed_workers:    # create new job only if there aren't already enough jobs for this workplace
                        self.joblist.append(Job(workplace.job_name, workplace.id, workplace.wage, workplace.job_skill, workplace.job_duration))
        
        # if there are more jobs then unemployed colonists, shorten joblist by removing jobs with lowest wages
        # TODO: check, if this is a sensible thing to do
        self.joblist = sorted(self.joblist, key=attrgetter("wage")) # sort joblist by wage
        # debug print
        print "Length joblist %s, length freeworkforce %s" % (len(self.joblist), len(self.freeworkforce))
        if len(self.freeworkforce) < len(self.joblist):
            dif = len(self.joblist)-len(self.freeworkforce)
            del self.joblist[-dif:]
        
        # Assign jobs to unemployed colonists
        for job in self.joblist:
            if job.worker == 0:     # assign only jobs, which aren't already assigned
                # debug print
                print "Job without worker found!"
                # sort colonistlist by relevant skill
                relevant_skill = job.skill
                self.colonistlist = sorted(self.colonistlist, key=lambda x: x.stock[relevant_skill], reverse=True)
                # assign job to the unemployed colonist with highest relevant skill
                for colonist in self.colonistlist:
                    if colonist.job == "Unemployed":
                        # debug print
                        print "Unemployed colonist found!"
                        colonist.job = job.name
                        job.assign_worker(colonist.id)
                        job.worker = 1
                        # add worker to workplace
                        # TODO: add job to workplace, so workplace can query employed colonists for skills etc
                        for workplace in self.workplacelist:
                            if workplace.id == job.workplace_id:
                                workplace.contracted_workers = workplace.contracted_workers + 1
                                workplace.initialize_production()   # to recalculate workers
                        self.freeworkforce.remove(colonist.id)
                        break
                    else:
                        # debug print
                        print "Colonist %s is already employed!" % (colonist.id)
            else:
                pass
        
        # Update existing jobs
        for job in self.joblist:
            if job.worker == 1 and job.duration > 0:
                
                # deduct wages
                # TODO: instead from central state, deduct wages from workplace
                newmoney = self.central_state.get_money() - job.wage
                self.central_state.set_money(newmoney)
                for colonist in self.colonistlist:
                    if colonist.id == job.colonist_id:
                        # pay wages
                        newmoney = colonist.get_money() + job.wage
                        colonist = colonist.set_money(newmoney)
                
                job.update_job()
            else:
                # delete job without worker or left duration from joblist
                for colonist in self.colonistlist:
                    if colonist.id == job.colonist_id:
                        colonist.job = "Unemployed"
                # remove worker from workplace
                for workplace in self.workplacelist:
                    if workplace.id == job.workplace_id:
                        workplace.contracted_workers -= 1
                        workplace.initialize_production()   # to recalculate workers
                self.joblist.remove(job)
            
            # debug print
            try:
                cid = job.colonist_id
            except AttributeError:
                cid = 0
            print "Job %s, workplace %s, worker %s, wage %s, skill %s, duration %s, colonist %s" % (job.name, job.workplace_id, job.worker, job.wage, job.skill, job.duration, cid)
                    


class Job(object):

    def __init__(self, name, id, wage, job_skill, job_duration):
        self.name = name
        self.workplace_id = id
        self.worker = 0
        self.wage = wage
        self.skill = job_skill
        self.duration = job_duration
        
    def assign_worker(self, colonist_id):
        self.worker = 1
        self.colonist_id = colonist_id

    def update_job(self):
        if self.duration > 0:
            self.duration -= 1