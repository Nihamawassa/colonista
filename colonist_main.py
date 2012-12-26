'''
Created on 22.08.2012

@author: JR
'''

from game_model import GameModel
from game_screen import GameScreen
from Tkinter import Tk


class ColonistGame(object):
    def __init__(self):
        pass

    def initialize_game(self):
        #initialize model instances
        print "initialize game"
        self.model_instance = GameModel()
        for colonist in self.model_instance.colonistlist:
            print colonist.get_name()

        self.root = Tk()
        self.app = GameScreen(self.root, game_instance)
        self.root.mainloop()
        self.app.update_screen()

    def next_turn(self):
        """
        Model update
        """
        self.model_instance.resolve_turn_phase()

        """
        Screen update
        """
        self.app.update_screen()

        print "Next turn"


if __name__ == '__main__':
    game_instance = ColonistGame()
    game_instance.initialize_game()
