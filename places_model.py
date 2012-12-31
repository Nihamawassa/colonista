'''
Created on 04.09.2012

@author: JR
'''


class Place(object):
    def __init__(self, x, y):
        self.x_coord = x
        self.y_coord = y
        self.name = "Open field"

    def set_place(self, x, y):
        self.x_coord = x
        self.y_coord = y

    def get_place(self):
        return Place(self.x_coord, self.y_coord)

    def set_placename(self, name):
        self.name = name

    def get_placename(self):
        return self.name


class Building(Place):

    def __init__(self, gamemodel, x, y):
        Place.__init__(self, x, y)

        self.gm = gamemodel
        self.ID = 0
        self.name = "Default"
        self.owner = self.gm.nature
        self.prize = 0
        self.storage = {}

        # Register new building in the building dictionary
        self.ID = self.gm.get_building_ID()
        if self.ID in self.gm.buildingdict:
            print "Error: duplicate ID in buildinglist"
        else:
            self.gm.buildingdict[self.ID] = self

    def get_owner(self):
        return self.owner

    def change_owner(self, oldowner, newowner):
        """ TODO: Implement sales tax at this place
        """
        if self.prize > 0:
            nomoney = newowner.get_money()
            newowner.set_money(nomoney - self.prize)
            oomoney = oldowner.get_money()
            oldowner.set_money(oomoney + self.prize)
        self.owner = newowner


class House(Building):

    def __init__(self, gamemodel, x, y, newowner):
        Building.__init__(self, gamemodel, x, y)

        self.name = "House"
        self.set_placename(self.name)
        oldowner = self.owner
        self.change_owner(oldowner, newowner)


class TradingPost(Building):

    def __init__(self, gamemodel, x, y):
        Building.__init__(self, gamemodel, x, y)

        self.name = "Trading Post"
        self.change_owner(self.owner, self.gm.state)


class Workplace(Building):

    def __init__(self, gamemodel, x, y, newowner, id):
        Building.__init__(self, gamemodel, x, y)
        oldowner = self.owner
        self.change_owner(oldowner, newowner)
        self.id = id

        self.active = True

    def update_workplace(self):
        if self.active:
            # perform update according to process rule
            pass
        else:
            pass


class Farm(Workplace):

    def __init__(self, gamemodel, x, y, newowner, id):
        Workplace.__init__(self, gamemodel, x, y, newowner, id)

        self.name = "Farm"
        self.set_placename(self.name)
        self.job_name = "farmwork"

        # input factors and coefficients
        self.fields = 1
        self.field_technology = 1
        self.needed_workers = 0
        self.contracted_workers = 0
        self.worker_skill = 0

        # output factors and coefficients
        self.food = 0
        self.food_output = 3

    def expand_farm(self):
        self.fields += 1
    
    def initialize_production(self):
        if self.active == True:
            self.needed_workers = self.fields
    
    def update_workplace(self):
        if self.active == True:
            Workplace.update_workplace(self)
            self.make_labor_contracts()
            self.calculate_output()
            self.calculate_costs()

    def make_labor_contracts(self):
        pass

    def calculate_output(self):
        """Production function
        Use Leontief production function for output calculation.
        """
        input1 = self.fields / (self.field_technology * 1)
        input2 = self.contracted_workers / (self.worker_skill * 1)
        self.food = self.food + self.food_output * min(input1, input2)

    def calculate_costs(self):
        pass

