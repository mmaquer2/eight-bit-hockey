import pygame, sys
from player import Player
from puck import Puck


class Rink:

    def __init__(self, screen):
        
        # rink animation and layout vars
        self.goal_one_location = 0
        self.goal_two_location = 0
        
        # game state vars
        self.game_running = False
        self.a_team_score = 0
        self.b_team_score = 0

        self.player = Player(screen, 5 , 5)

        #self.setup() # execute game setup


    def setup(self):

        # setup the rink 
        
        # TODO:
        # Team Benches
        # Crowd and Background
        # Scoreboard 
        


        # setup scoreboard

        # setup player 1

        # setup puck

        # setup team a

        # setup team b

        
        pass

        
    def start(self):
        self.game_running = True

        # trigger first puck drop
        # start_puck_drop()

    def run(self):
        
        while self.game_running:
            self.update()
            print("Update Game Actions")

    def update(self):
        
        self.player.update()


