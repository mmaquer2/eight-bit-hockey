import pygame, sys

class Puck:
    def __init__(self, window, start_x, start_y):
        self.screen = window
        self.pos_x = start_x
        self.pos_y = start_y
        
        self.pos = pygame.Vector2()
        self.setup()

    def setup(self):
        pass

    def update(self):
        self.pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
        pygame.draw.circle(self.screen, "black", self.pos, 5)