import pygame, sys
from rink import Rink

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 400, 800 

# Rink dimensions
RINK_WIDTH = WIDTH - 50
RINK_HEIGHT = HEIGHT - 100
RINK_X = 25
RINK_Y = 50
GOAL_WIDTH = 10
GOAL_HEIGHT = 60
GOAL_DEPTH = 20

# Line widths
LINE_WIDTH = 5
CIRCLE_WIDTH = 2


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Eight Bit Hockey')
        game_window = (800,1200)
        self.screen = pygame.display.set_mode(game_window)
        self.background = pygame.Surface(game_window)
        self.screen.blit(self.background, (0,0))
        self.paused = False

        self.rink = Rink(self.screen)

    def run(self):

        # Main Game Loop
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
                

            # update block            
            if not self.paused:
                
                self.draw_rink()
                self.rink.update();   # update the rink at each tick
                
                pygame.display.update()
                
    def draw_rink(self):
        surface = self.screen        
        # Fill the background
        surface.fill(WHITE)

        # Dimensions for the game window
        GAME_WIDTH, GAME_HEIGHT = 800, 1200

        # Center the rink dynamically in the game window
        rink_x = (GAME_WIDTH - RINK_WIDTH) // 2
        rink_y = (GAME_HEIGHT - RINK_HEIGHT) // 2


        # Draw the rink boundary
        pygame.draw.rect(surface, BLACK, (rink_x, rink_y, RINK_WIDTH, RINK_HEIGHT), LINE_WIDTH, border_radius=50)

        # Center line
        pygame.draw.line(surface, RED, (rink_x, rink_y + RINK_HEIGHT // 2), (rink_x + RINK_WIDTH, rink_y + RINK_HEIGHT // 2), LINE_WIDTH)

        # Blue lines
        pygame.draw.line(surface, BLUE, (rink_x, rink_y + RINK_HEIGHT // 3), (rink_x + RINK_WIDTH, rink_y + RINK_HEIGHT // 3), LINE_WIDTH)
        pygame.draw.line(surface, BLUE, (rink_x, rink_y + 2 * RINK_HEIGHT // 3), (rink_x + RINK_WIDTH, rink_y + 2 * RINK_HEIGHT // 3), LINE_WIDTH)

        # Center circle
        center_x = rink_x + RINK_WIDTH // 2
        center_y = rink_y + RINK_HEIGHT // 2
        pygame.draw.circle(surface, RED, (center_x, center_y), 50, CIRCLE_WIDTH)

        # Offensive and defensive faceoff circles
        self.draw_faceoff_zones(surface, rink_y + RINK_HEIGHT // 6, True)  # Top offensive zone
        self.draw_faceoff_zones(surface, rink_y + 5 * RINK_HEIGHT // 6, False)  # Bottom offensive zone

        # Goal areas
        self.draw_goal(surface, WIDTH // 2 - GOAL_HEIGHT // 2, rink_y - GOAL_DEPTH + 50, True)  # Top goal
        self.draw_goal(surface, WIDTH // 2 - GOAL_HEIGHT // 2, rink_y + RINK_HEIGHT - 50, False)  # Bottom goal


      
    def draw_faceoff_zones(self, surface, zone_center_y, is_top_zone):
        # Rink's dynamic position
        GAME_WIDTH, GAME_HEIGHT = 800, 1200
        rink_x = (GAME_WIDTH - RINK_WIDTH) // 2

        # Faceoff circle positions
        offset_x = RINK_WIDTH // 4
        left_faceoff = (rink_x + offset_x, zone_center_y)
        right_faceoff = (rink_x + RINK_WIDTH - offset_x, zone_center_y)

        # Draw faceoff circles
        pygame.draw.circle(surface, RED, left_faceoff, 40, CIRCLE_WIDTH)
        pygame.draw.circle(surface, RED, right_faceoff, 40, CIRCLE_WIDTH)

        # Draw faceoff dots
        pygame.draw.circle(surface, RED, left_faceoff, 5)
        pygame.draw.circle(surface, RED, right_faceoff, 5)


    def draw_goal(self, surface, x, y, is_top_goal):
        GAME_WIDTH, GAME_HEIGHT = 800, 1200
        rink_x = (GAME_WIDTH - RINK_WIDTH) // 2

        # Adjust x dynamically for the centered rink
        goal_x = rink_x + (RINK_WIDTH - GOAL_HEIGHT) // 2
        
        
        # TODO: draw goal crease
        # TODO: draw rink goal lines
        
        if is_top_goal:
            #pygame.draw.line(surface, RED, (RINK_X, RINK_Y + RINK_HEIGHT // 12), (RINK_X + RINK_WIDTH, RINK_Y + RINK_HEIGHT // 12), LINE_WIDTH)
            #pygame.draw.arc(surface,BLUE,)
            pass
        
        else:
            #pygame.draw.line(surface, RED, (RINK_X, HEIGHT - 10), (RINK_X + RINK_WIDTH, HEIGHT - 10), LINE_WIDTH)
            #pygame.draw.arc(surface,BLUE,)
            pass

        # Draw the goal frame
        pygame.draw.rect(surface, RED, (goal_x, y, GOAL_HEIGHT, GOAL_DEPTH), 2)

        # Draw the net
        for i in range(5, GOAL_HEIGHT, 5):
            pygame.draw.line(surface, BLUE, (goal_x + i, y), (goal_x + i, y + GOAL_DEPTH), 1)
        for j in range(5, GOAL_DEPTH, 5):
            pygame.draw.line(surface, BLUE, (goal_x, y + j), (goal_x + GOAL_HEIGHT, y + j), 1)



