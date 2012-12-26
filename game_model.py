'''
Created on 26.08.2012

@author: JR
'''

from agents_model import Nature, CentralState, Colonist
from places_model import TradingPost, House


class GameModel(object):
    def __init__(self):
        self.calendar_instance = Calendar()
        self.nature = Nature(self)
        self.state = CentralState(self)

        self.colonist_counter = 0
        self.colonistlist = [self.create_colonist("Adam"), self.create_colonist("Berta"),
                             self.create_colonist("Carl"), self.create_colonist("Dorothy"),
                             self.create_colonist("Elmer"), self.create_colonist("Faye"),
                             self.create_colonist("Gordon"), self.create_colonist("Hilma"),
                             self.create_colonist("Igor")]

        self.buildingID = 1
        self.buildingdict = {0: "dummy"}
        self.buildingdict = {1: House(self, 0, 0, self.colonistlist[0]),
                             2: House(self, 0, 1, self.colonistlist[1]),
                             3: House(self, 0, 2, self.colonistlist[2]),
                             4: House(self, 0, 3, self.colonistlist[3]),
                             5: House(self, 0, 4, self.colonistlist[4]),
                             6: House(self, 0, 5, self.colonistlist[5]),
                             7: House(self, 0, 6, self.colonistlist[6]),
                             8: House(self, 0, 7, self.colonistlist[7]),
                             9: House(self, 0, 8, self.colonistlist[8])}
        self.tradingpost = TradingPost(self, 0, 9)
        self.tradingpost.store = {"money": 1000, "food": 1000,
                                  "clothing": 1000}
        self.pricelist = {"food": 10, "clothing": 10}

    def create_colonist(self, name):
        self.colonist_counter += 1
        colonist = Colonist(self, name, self.colonist_counter)
        return colonist

    def get_building_ID(self):
        self.buildingID += 1
        return self.buildingID

    def resolve_turn_phase(self):
        self.calendar_instance.increase_time()
        for colonist in self.colonistlist:
            colonist.update_colonist()


class Calendar(object):
    """
    1 year has 4 seasons, 1 season has 10 days
    """

    def __init__(self):
        self.time = 0
        self.seasonnames = ["Winter", "Spring", "Summer", "Autumn"]

    def increase_time(self):
        self.time = self.time + 1
        print self.time
        print "The new date is " + self.days_to_date_string()

    def get_time(self):
        return self.time

    def get_year(self):
        year = int(self.time / 40)
        return year

    def get_season(self):
        season_int = int((self.time - (self.get_year() * 40)) / 10)
        return season_int

    def get_day_in_year(self):
        day_in_year_int = self.time - (self.get_year() * 40) - (self.get_season() * 10)
        return day_in_year_int

    def days_to_date_string(self):
        return "year " + str(self.get_year()) + ", season " + self.seasonnames[
            self.get_season()] + ", day " + str(self.get_day_in_year())
