import pygame
import sys
from rink import Rink

class GameConstants:
    # Colors
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    
    # Window dimensions
    GAME_WIDTH = 800
    GAME_HEIGHT = 1200
    
    # Rink dimensions
    RINK_WIDTH = 350  # WIDTH - 50
    RINK_HEIGHT = 700  # HEIGHT - 100
    
    # Goal dimensions
    GOAL_WIDTH = 10
    GOAL_HEIGHT = 60
    GOAL_DEPTH = 20
    
    # Line properties
    LINE_WIDTH = 5
    CIRCLE_WIDTH = 2
    
    # Gameplay constants
    FACEOFF_CIRCLE_RADIUS = 40
    CENTER_CIRCLE_RADIUS = 50
    FACEOFF_DOT_RADIUS = 5
    FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Eight Bit Hockey')
        
        self.screen = pygame.display.set_mode((GameConstants.GAME_WIDTH, GameConstants.GAME_HEIGHT))
        self.background = pygame.Surface((GameConstants.GAME_WIDTH, GameConstants.GAME_HEIGHT))
        self.screen.blit(self.background, (0, 0))
        self.clock = pygame.time.Clock()
        self.paused = False
        self.rink = Rink(self.screen)
        
        # Calculate rink position once
        self.rink_x = (GameConstants.GAME_WIDTH - GameConstants.RINK_WIDTH) // 2
        self.rink_y = (GameConstants.GAME_HEIGHT - GameConstants.RINK_HEIGHT) // 2

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Escape Key Pressed Quitting Game...")
                    return False
                elif event.key == pygame.K_p:
                    print("Game Paused!")
                    self.paused = True
                elif event.key == pygame.K_u:
                    print("Game Unpaused!")
                    self.paused = False
        return True

    def run(self):
        running = True
        while running:
            # Calculate delta time in seconds
            dt = self.clock.tick(GameConstants.FPS) / 1000.0
            
            running = self.handle_events()
            
            if not self.paused:
                self.draw_rink()
                self.rink.update(dt)  # Pass dt to rink update
                pygame.display.update()
            
        pygame.quit()
        sys.exit()

    def draw_rink(self):
        # Fill background
        self.screen.fill(GameConstants.WHITE)
        
        # Draw main rink outline
        pygame.draw.rect(self.screen, GameConstants.BLACK, 
                        (self.rink_x, self.rink_y, 
                         GameConstants.RINK_WIDTH, GameConstants.RINK_HEIGHT),
                        GameConstants.LINE_WIDTH, border_radius=50)
        
        self._draw_lines()
        self._draw_center_circle()
        self._draw_faceoff_zones()
        self._draw_goals()

    def _draw_lines(self):
        # Center line
        center_y = self.rink_y + GameConstants.RINK_HEIGHT // 2
        pygame.draw.line(self.screen, GameConstants.RED,
                        (self.rink_x, center_y),
                        (self.rink_x + GameConstants.RINK_WIDTH, center_y),
                        GameConstants.LINE_WIDTH)
        
        # Blue lines
        for i in range(1, 3):
            y_pos = self.rink_y + (i * GameConstants.RINK_HEIGHT // 3)
            pygame.draw.line(self.screen, GameConstants.BLUE,
                           (self.rink_x, y_pos),
                           (self.rink_x + GameConstants.RINK_WIDTH, y_pos),
                           GameConstants.LINE_WIDTH)

    def _draw_center_circle(self):
        center_x = self.rink_x + GameConstants.RINK_WIDTH // 2
        center_y = self.rink_y + GameConstants.RINK_HEIGHT // 2
        pygame.draw.circle(self.screen, GameConstants.RED,
                         (center_x, center_y),
                         GameConstants.CENTER_CIRCLE_RADIUS,
                         GameConstants.CIRCLE_WIDTH)

    def _draw_faceoff_zones(self):
        # Top and bottom faceoff zones
        zones = [
            self.rink_y + GameConstants.RINK_HEIGHT // 6,  # Top
            self.rink_y + 5 * GameConstants.RINK_HEIGHT // 6  # Bottom
        ]
        
        for zone_y in zones:
            offset_x = GameConstants.RINK_WIDTH // 4
            for x_pos in [self.rink_x + offset_x, self.rink_x + GameConstants.RINK_WIDTH - offset_x]:
                # Draw circle
                pygame.draw.circle(self.screen, GameConstants.RED,
                                (x_pos, zone_y),
                                GameConstants.FACEOFF_CIRCLE_RADIUS,
                                GameConstants.CIRCLE_WIDTH)
                # Draw dot
                pygame.draw.circle(self.screen, GameConstants.RED,
                                (x_pos, zone_y),
                                GameConstants.FACEOFF_DOT_RADIUS)

    def _draw_goals(self):
        goal_positions = [
            (self.rink_y - GameConstants.GOAL_DEPTH + 50, True),  # Top goal
            (self.rink_y + GameConstants.RINK_HEIGHT - 50, False)  # Bottom goal
        ]
        
        for y_pos, is_top in goal_positions:
            goal_x = self.rink_x + (GameConstants.RINK_WIDTH - GameConstants.GOAL_HEIGHT) // 2
            
            # Draw goal frame
            pygame.draw.rect(self.screen, GameConstants.RED,
                           (goal_x, y_pos, GameConstants.GOAL_HEIGHT, GameConstants.GOAL_DEPTH), 2)
            
            # Draw net lines
            for i in range(5, GameConstants.GOAL_HEIGHT, 5):
                pygame.draw.line(self.screen, GameConstants.BLUE,
                               (goal_x + i, y_pos),
                               (goal_x + i, y_pos + GameConstants.GOAL_DEPTH), 1)
            for j in range(5, GameConstants.GOAL_DEPTH, 5):
                pygame.draw.line(self.screen, GameConstants.BLUE,
                               (goal_x, y_pos + j),
                               (goal_x + GameConstants.GOAL_HEIGHT, y_pos + j), 1)

if __name__ == "__main__":
    game = Game()
    game.run()