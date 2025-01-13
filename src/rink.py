import pygame, sys
from player import Player
from puck import Puck


class Rink:
    def __init__(self, screen):
        self.screen = screen  
        
        # Calculate center position for player start
        start_x = screen.get_width() // 2
        start_y = screen.get_height() // 2
        
        # Initialize game state vars
        self.game_running = False
        self.a_team_score = 0
        self.b_team_score = 0
        
        # Initialize teams and actors
        self.team_a = []
        self.team_b = []
        self.actors = []
        
        # Create player at center
        self.player = Player(screen, start_x, start_y)
        self.actors.append(self.player)  # Add player to actors list
        
        # Rink layout vars
        self.goal_one_location = 0
        self.goal_two_location = 0

    def setup(self):
        # Your existing setup code...
        pass

    def start(self):
        self.game_running = True

    def run(self):
        while self.game_running:
            self.update()

    def update(self, dt):
        # Update all actors
        for actor in self.actors:
            actor.update(dt)
            
        # Draw all actors
        self.draw()
    
    def draw(self):
        # Draw all actors
        for actor in self.actors:
            actor.draw()