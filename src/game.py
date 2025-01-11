import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Eight Bit Hockey')
        game_window = (1280, 736)
        self.screen = pygame.display.set_mode(game_window)
        self.background = pygame.Surface(game_window)
        self.screen.blit(self.background, (0,0))

        self.paused = False


    def run(self):
        while True:   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("Escape Key Pressed Quitting Game...")
                        pygame.quit()
                        sys.exit()

                
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            print("Game Paused!")
                            self.paused = True
                
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_u:
                            print("Game Unaused!")
                            self.paused = False
                
                
            if not self.paused:
                    
                self.screen.fill('light green') # background color
                
                #self.level.run();   # update the level at each tick
                pygame.display.update()
                #self.clock.tick(FPS)