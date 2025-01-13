import pygame, sys

class Player:

    def __init__(self, window, start_x, start_y):
        self.screen = window
        self.x = 0
        self.y = 0
        
        self.direction = pygame.math.Vector2()

        ## action status:


    def start(self):
        pass

    def input(self):
        pass

    def input(self):
        keys = pygame.key.get_pressed()

        print(keys)


    def move(self):
        pass

    def update(self):

        #self.get_status()
        #self.input()
        #self.animate()
        #self.move()

        # handle user input and player animations

        player_pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
        pygame.draw.circle(self.screen, "purple", player_pos, 10)


        
        


    

