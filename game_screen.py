'''
Created on 26.08.2012

@author: JR
'''

from Tkinter import *


class GameScreen(object):

    def __init__(self, master, gameinstance):

        self.gi = gameinstance

        content = Frame(master)
        frame1 = Frame(content, bd=3, relief=GROOVE)
        frame2 = Frame(content, bd=3, relief=GROOVE)
        frame3 = Frame(content, bd=3, relief=GROOVE)
        frame4 = Frame(content, bd=3, relief=GROOVE)
        frame5 = Frame(content, bd=3, relief=GROOVE)
        frame6 = Frame(content, bd=3, relief=GROOVE)
        frame7 = Frame(content, bd=3, relief=GROOVE)
        frame8 = Frame(content, bd=3, relief=GROOVE)
        frame9 = Frame(content, bd=3, relief=GROOVE)

        content.grid(column=0, row=0, sticky=(N, S, E, W))
        frame1.grid(row=0, column=0)
        frame2.grid(row=0, column=1)
        frame3.grid(row=0, column=2)
        frame4.grid(row=1, column=0)
        frame5.grid(row=1, column=1)
        frame6.grid(row=1, column=2)
        frame7.grid(row=2, column=0)
        frame8.grid(row=2, column=1)
        frame9.grid(row=2, column=2)

        framelist = [frame1, frame2, frame3, frame4, frame5, frame6, frame7,
                     frame8, frame9]

        self.button = Button(content, text="QUIT", fg="red",
                             command=master.quit)
        self.button.grid(row=3, column=0)
        self.turn = Button(content, text="Next Turn",
                           command=self.gi.next_turn)
        self.turn.grid(row=3, column=1)

        self.v = StringVar()
        self.datelabel = Label(content, textvariable=self.v)
        self.datelabel.grid(row=3, column=2)

        self.namelist = []
        self.healthlist = []
        self.agelist = []
        self.foodlist = []
        self.clothinglist = []
        self.moneylist = []
        self.joblist = []
        self.skilllist = []
        self.placelist = []

        i = 0
        for colonist in self.gi.model_instance.colonistlist:
            name = StringVar()
            name.set(colonist.name)
            self.namelist.append(name)
            health = StringVar()
            health.set(colonist.stock["health"])
            self.healthlist.append(health)
            age = StringVar()
            age.set(colonist.age)
            self.agelist.append(age)
            food = StringVar()
            food.set(colonist.stock["food"])
            self.foodlist.append(food)
            clothing = StringVar()
            clothing.set(colonist.stock["clothing"])
            self.clothinglist.append(clothing)
            money = StringVar()
            money.set(colonist.stock["money"])
            self.moneylist.append(money)
            job = StringVar()
            job.set(colonist.job)
            self.joblist.append(job)
            skill = StringVar()
            skill.set(colonist.stock["farmingSkill"])
            self.skilllist.append(skill)
            place = StringVar()
            place.set(colonist.place.get_placename())
            self.placelist.append(place)

            masterframe = framelist[i]
            Label(masterframe, text="Image Placeholder").grid(row=0, column=0,
                                                              columnspan=2,
                                                              rowspan=3)

            Label(masterframe, text="Name: ").grid(row=3, column=0)
            namelabel = Label(masterframe, textvariable=name)
            namelabel.grid(row=3, column=1)

            Label(masterframe, text="Health: ").grid(row=4, column=0)
            healthlabel = Label(masterframe, textvariable=health)
            healthlabel.grid(row=4, column=1)

            Label(masterframe, text="Age: ").grid(row=5, column=0)
            agelabel = Label(masterframe, textvariable=age)
            agelabel.grid(row=5, column=1)

            Label(masterframe, text="Food: ").grid(row=0, column=2)
            foodlabel = Label(masterframe, textvariable=food)
            foodlabel.grid(row=0, column=3)

            Label(masterframe, text="Clothing: ").grid(row=1, column=2)
            clothinglabel = Label(masterframe, textvariable=clothing)
            clothinglabel.grid(row=1, column=3)

            Label(masterframe, text="Money: ").grid(row=2, column=2)
            moneylabel = Label(masterframe, textvariable=money)
            moneylabel.grid(row=2, column=3)

            Label(masterframe, text="Job: ").grid(row=3, column=2)
            joblabel = Label(masterframe, textvariable=job)
            joblabel.grid(row=3, column=3)

            Label(masterframe, text="Skill: ").grid(row=4, column=2)
            skilllabel = Label(masterframe, textvariable=skill)
            skilllabel.grid(row=4, column=3)

            Label(masterframe, text="Place: ").grid(row=5, column=2)
            placelabel = Label(masterframe, textvariable=place)
            placelabel.grid(row=5, column=3)

            i += 1

    def update_screen(self):
        datestring = self.gi.model_instance.calendar_instance.days_to_date_string()
        self.v.set(datestring)
        i = 0
        while i < 9:
            self.namelist[i].set(self.gi.model_instance.colonistlist[i].get_name())
            self.healthlist[i].set(self.gi.model_instance.colonistlist[i].stock["health"])
            self.agelist[i].set(self.gi.model_instance.colonistlist[i].age)
            self.foodlist[i].set(self.gi.model_instance.colonistlist[i].stock["food"])
            self.clothinglist[i].set(self.gi.model_instance.colonistlist[i].stock["clothing"])
            self.moneylist[i].set(self.gi.model_instance.colonistlist[i].stock["money"])
            self.joblist[i].set(self.gi.model_instance.colonistlist[i].job)
            self.skilllist[i].set(self.gi.model_instance.colonistlist[i].stock["farmingSkill"])
            self.placelist[i].set(self.gi.model_instance.colonistlist[i].placename)
            i += 1


# root = Tk()

# app = GameScreen(root)

# root.mainloop()
