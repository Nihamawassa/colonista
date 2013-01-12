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
        self.stock["farming_skill"] = 1          # range 1-99
        self.stock["handcrafting_skill"] = 1     # range 1-99
        
        self.shopping_list = {}

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
    
    def calculate_good(self, name):
        '''Calculate available good
        '''
        ownedbuildings = self.get_owned_buildings()
        availablegood = self.stock[str(name)]
        for building in ownedbuildings:
            availablegood += building.storage.get(str(name), 0)
        return availablegood
    
    def buy_good(self, name, amount):
        price = self.gm.pricelist[str(name)]
        if self.get_money() < (amount * price):
            amount = int(self.get_money() / price)
        goods = self.gm.tradingpost.sell_storage(str(name), amount)
        self.set_money(self.get_money() - (goods * price))
        return goods

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
        
        # debug print
        print "Colonist %s, name %s, job %s, money %s, food %s, health %s" % (self.id, self.name, self.job, self.stock["money"], self.stock["food"], self.stock["health"])

    def update_AI(self):
        '''Update AI
        '''
        
        # Update daily AI
        
        # Update seasonal AI
        if self.gm.calendar_instance.get_day_in_year() == 0:
           
            seasonalfood = 10
            
            # Calculate available food.
            availablefood = self.calculate_good("food")

            # Calculate available clothing.
            availableclothing = self.calculate_good("clothing")

            # Populate shopping list
            neededfood = seasonalfood - availablefood
            if neededfood > 0:
                self.shopping_list["food"] = neededfood
                
            # Buy food
            self.stock["food"] = self.stock["food"] + self.buy_good("food", neededfood)
        
        # Update yearly AI
        if (self.gm.calendar_instance.get_season() == 0) & (self.gm.calendar_instance.get_day_in_year() == 0):
            """ Update AI according to Maslov's pyramid. Calculate replenishment
            of personal stock.
            """
            
            yearlyfood = 40 * 2 + 20   # food for 40 days plus 20 reserve
            yearlyclothing = 40 * 2 + 20

            # Calculate available food.
            availablefood = self.calculate_good("food")

            # Calculate available clothing.
            availableclothing = self.calculate_good("clothing")

            # Populate shopping list
            neededfood = yearlyfood - availablefood
            if neededfood <= 0:
                neededfood = 0
            else:
                self.shopping_list["food"] = neededfood
            # Buy food
            self.stock["food"] = self.stock["food"] + self.buy_good("food", neededfood)
                
                
            neededclothing = yearlyclothing - availableclothing
            if neededclothing < 0:
                neededclothing = 0

            neededmoney = (neededfood * self.gm.pricelist["food"]) + (neededclothing * self.gm.pricelist["clothing"])
            print "This year, colonist " + self.name + " needs " + str(neededmoney) + " money."
            
    
