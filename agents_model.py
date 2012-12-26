'''
Created on 22.08.2012

@author: JR
'''

from places_model import Place


class Agent(object):

    def __init__(self, gamemodel):
        self.gm = gamemodel
        self.stock = {"money": 0}          # range 0-999999

    def get_money(self):
        return self.stock["money"]

    def set_money(self, newmoney):
        if newmoney >= 0:
            self.stock["money"] = newmoney
        else:
            print "Error: tried to set a negative money value"


class Nature(Agent):

    def __init__(self, gamemodel):
        Agent.__init__(self, gamemodel)


class CentralState(Agent):

    def __init__(self, gamemodel):
        Agent.__init__(self, gamemodel)
        self.stock["food"] = 100
        self.stock["clothing"] = 100
        Agent.set_money(self, 1000)

    def update_centralstate(self):
        pass


class Colonist(Agent):

    def __init__(self, gamemodel, colname, id):
        Agent.__init__(self, gamemodel)
        self.name = colname
        self.id = id
        self.age = 1                        # range 0-999999 in days
        self.job = "Unemployed"
        self.state = "Alive"

        self.place = Place(0, 0)            # TODO: check for position first
        self.placename = self.place.get_placename()

        self.stock["health"] = 99               # range 0-99
        self.stock["food"] = 20                 # range 0-20
        self.stock["clothing"] = 80             # range 0-80
        self.stock["farmingSkill"] = 0          # range 0-99
        self.stock["handcraftingSkill"] = 0     # range 0-99

    def get_name(self):
        return self.name

    def goto_place(self, newplace):
        self.place = newplace

    def get_owned_buildings(self):
        owned_buildings = []
        for i in self.gm.buildingdict:
            owner = self.gm.buildingdict[i].get_owner()
            if owner == self:
                owned_buildings.append(self.gm.buildingdict[i])
        return owned_buildings

    def update_colonist(self):
        if self.state != "Dead":
            self.update_AI()
            self.age += 1
            if self.stock["food"] > 0:
                self.stock["food"] -= 1
            if self.stock["clothing"] > 0:
                self.stock["clothing"] -= 1
            if self.stock["food"] <= 0:
                self.stock["health"] -= 1
            if self.stock["health"] <= 0:
                self.state = "Dead"

    def update_AI(self):
        """ Update yearly AI.
        """
        if (self.gm.calendar_instance.get_season() == 0) & (self.gm.calendar_instance.get_day_in_year() == 0):
            """ Update AI according to Maslov's pyramid. Calculate replenishment
            of personal stock.
            """
            ownedbuildings = self.get_owned_buildings()
            yearlyfood = 40 * 2 + 20   # food for 40 days plus 20 reserve
            yearlyclothing = 40 * 2 + 20

            """ Calculate available food.
            """
            availablefood = self.stock["food"]
            for building in ownedbuildings:
                availablefood += building.storage.get("food", 0)

            """Calculate available clothing.
            """
            availableclothing = self.stock["clothing"]
            for building in ownedbuildings:
                availableclothing += building.storage.get("clothing", 0)

            neededfood = yearlyfood - availablefood
            if neededfood < 0:
                neededfood = 0
            neededclothing = yearlyclothing - availableclothing
            if neededclothing < 0:
                neededclothing = 0

            neededmoney = (neededfood * self.gm.pricelist["food"]) + (neededclothing * self.gm.pricelist["clothing"])
            print "This year, colonist " + self.name + " needs " + str(neededmoney) + " money."

        """ Update seasonal AI.
        """

        """ Update daily AI
        """
