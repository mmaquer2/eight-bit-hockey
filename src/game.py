import pygame
import sys
from rink import Rink
from puck import Puck
from camera import Camera
from player import Player

class GameConstants:
    # Colors
    WHITE = (255, 255, 255)
    BLUE = (0, 102, 204)    # Darker blue for lines
    RED = (204, 0, 0)       # Darker red for lines
    BLACK = (0, 0, 0)
    ICE_COLOR = (220, 240, 255)  # Slight blue tint for ice
    
    # Base resolution and scaling
    BASE_WIDTH = 800
    BASE_HEIGHT = 1200
    
    # Camera and View
    DEFAULT_ZOOM = 1.5      # Closer view like NHL '94
    VERTICAL_OFFSET = 0.2   # Show more of the attacking zone
    
    # Rink proportions
    RINK_WIDTH_RATIO = 0.35  # Narrower rink
    RINK_HEIGHT_RATIO = 0.8  # Taller rink for better view
    
    # Goal proportions (as percentages of rink)
    GOAL_WIDTH_RATIO = 0.02
    GOAL_HEIGHT_RATIO = 0.15
    GOAL_DEPTH_RATIO = 0.05
    
    # Line properties (scaled with screen size)
    LINE_WIDTH_RATIO = 0.006
    CIRCLE_WIDTH_RATIO = 0.003
    
    # Gameplay constants (scaled with rink size)
    FACEOFF_CIRCLE_RATIO = 0.15
    CENTER_CIRCLE_RATIO = 0.17
    FACEOFF_DOT_RATIO = 0.015
    FPS = 60
    
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Eight Bit Hockey')
        
        self.screen = pygame.display.set_mode((GameConstants.BASE_WIDTH, 
                                             GameConstants.BASE_HEIGHT), 
                                             pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.paused = False
        
        # Calculate initial dimensions
        self.update_dimensions()
        
        # Initialize camera with default zoom
        self.camera = Camera(GameConstants)
        self.camera.zoom = GameConstants.DEFAULT_ZOOM
        
        # Create game objects after dimensions are set
        self.init_game_objects()

    def init_game_objects(self):
        """Initialize all game objects with current dimensions"""
        # Calculate rink boundaries
        self.rink_bounds = {
            'left': self.rink_x,
            'right': self.rink_x + self.rink_width,
            'top': self.rink_y,
            'bottom': self.rink_y + self.rink_height
        }
        
        # Create player and puck with proper bounds
        self.player = Player(self.screen, GameConstants, self.rink_bounds)
        self.puck = Puck(self.screen, GameConstants, self.rink_bounds)

    def update_dimensions(self):
        """Update all dimensions based on current screen size"""
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        
        # Scale factor based on screen size
        self.scale_x = self.screen_width / GameConstants.BASE_WIDTH
        self.scale_y = self.screen_height / GameConstants.BASE_HEIGHT
        self.scale = min(self.scale_x, self.scale_y)
        
        # Calculate rink dimensions
        self.rink_width = int(self.screen_width * GameConstants.RINK_WIDTH_RATIO)
        self.rink_height = int(self.screen_height * GameConstants.RINK_HEIGHT_RATIO)
        
        # Calculate all the additional dimensions needed for drawing
        self.line_width = max(1, int(self.screen_width * GameConstants.LINE_WIDTH_RATIO))
        self.circle_width = max(1, int(self.screen_width * GameConstants.CIRCLE_WIDTH_RATIO))
        self.center_circle_radius = int(self.rink_width * GameConstants.CENTER_CIRCLE_RATIO)
        self.faceoff_circle_radius = int(self.rink_width * GameConstants.FACEOFF_CIRCLE_RATIO)
        self.faceoff_dot_radius = int(self.rink_width * GameConstants.FACEOFF_DOT_RATIO)
        self.goal_width = int(self.rink_width * GameConstants.GOAL_WIDTH_RATIO)
        self.goal_height = int(self.rink_height * GameConstants.GOAL_HEIGHT_RATIO)
        self.goal_depth = int(self.rink_width * GameConstants.GOAL_DEPTH_RATIO)
        
        # Calculate rink position with vertical offset
        self.rink_x = (self.screen_width - self.rink_width) // 2
        self.rink_y = int((self.screen_height - self.rink_height) * 
                        (0.5 + GameConstants.VERTICAL_OFFSET))

        # Update existing objects if they exist
        if hasattr(self, 'rink_bounds'):
            self.rink_bounds.update({
                'left': self.rink_x,
                'right': self.rink_x + self.rink_width,
                'top': self.rink_y,
                'bottom': self.rink_y + self.rink_height
            })

    def run(self):
        running = True
        while running:
            # Calculate delta time in seconds
            dt = self.clock.tick(GameConstants.FPS) / 1000.0
            
            running = self.handle_events()
            
            if not self.paused:
                self.update(dt)
                self.draw()
                pygame.display.update()
            
        pygame.quit()
        sys.exit()

    def update(self, dt):
        """Update game logic"""
        # Update player and puck
        self.player.move(dt)
        self.puck.update(dt)
        
        # Basic puck possession
        if self.player_can_get_puck():
            self.player.has_puck = True
            self.puck.pos = self.player.pos

    def player_can_get_puck(self):
        """Check if player is close enough to get puck"""
        distance = (self.player.pos - self.puck.pos).length()
        return distance < 20  # Adjust this value as needed

    def draw(self):
        """Draw everything"""
        # Fill background with ice color
        self.screen.fill(GameConstants.ICE_COLOR)
        
        # Draw rink
        self.draw_rink()
        
        # Draw game objects
        self.puck.draw()
        self.player.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), 
                                                    pygame.RESIZABLE)
                self.update_dimensions()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_p:
                    self.paused = True
                elif event.key == pygame.K_u:
                    self.paused = False
                # Add shooting controls
                elif event.key == pygame.K_SPACE and self.player.has_puck:
                    self.shoot_puck()
        return True

    def shoot_puck(self):
        """Handle puck shooting"""
        if self.player.has_puck:
            self.player.has_puck = False
            
            # If player is moving, shoot in movement direction
            if self.player.velocity.length() > 0:
                shoot_direction = self.player.velocity.normalize()
                self.puck.velocity = self.player.velocity * 2  # Keep momentum
            else:
                # If player is stationary, shoot based on player facing direction
                # For now, defaulting to shooting upward if no movement
                shoot_direction = pygame.math.Vector2(0, -1)
                self.puck.velocity = pygame.math.Vector2(0, 0)
            
            # Add shooting velocity
            shoot_speed = 500  # Adjust this value for shot power
            self.puck.velocity += shoot_direction * shoot_speed
            
    def draw_rink(self):
        # Draw main rink outline
        pygame.draw.rect(self.screen, GameConstants.BLACK, 
                        (self.rink_x, self.rink_y, 
                        self.rink_width, self.rink_height),
                        self.line_width, border_radius=int(50 * self.scale))
        
        self._draw_lines()
        self._draw_center_circle()
        self._draw_faceoff_zones()
        self._draw_goals()

    def _draw_lines(self):
        # Center line
        center_y = self.rink_y + self.rink_height // 2
        pygame.draw.line(self.screen, GameConstants.RED,
                        (self.rink_x, center_y),
                        (self.rink_x + self.rink_width, center_y),
                        self.line_width)
        
        # Blue lines
        for i in range(1, 3):
            y_pos = self.rink_y + (i * self.rink_height // 3)
            pygame.draw.line(self.screen, GameConstants.BLUE,
                        (self.rink_x, y_pos),
                        (self.rink_x + self.rink_width, y_pos),
                        self.line_width)

    def _draw_center_circle(self):
        center_x = self.rink_x + self.rink_width // 2
        center_y = self.rink_y + self.rink_height // 2
        pygame.draw.circle(self.screen, GameConstants.RED,
                        (center_x, center_y),
                        self.center_circle_radius,
                        self.circle_width)

    def _draw_faceoff_zones(self):
        # Top and bottom faceoff zones
        zones = [
            self.rink_y + self.rink_height // 6,  # Top
            self.rink_y + 5 * self.rink_height // 6  # Bottom
        ]
        
        for zone_y in zones:
            offset_x = self.rink_width // 4
            for x_pos in [self.rink_x + offset_x, self.rink_x + self.rink_width - offset_x]:
                pygame.draw.circle(self.screen, GameConstants.RED,
                                (x_pos, zone_y),
                                self.faceoff_circle_radius,
                                self.circle_width)
                pygame.draw.circle(self.screen, GameConstants.RED,
                                (x_pos, zone_y),
                                self.faceoff_dot_radius)

    def _draw_goals(self):
        goal_positions = [
            (self.rink_y - self.goal_depth + int(50 * self.scale), True),  # Top goal
            (self.rink_y + self.rink_height - int(50 * self.scale), False)  # Bottom goal
        ]
        
        for y_pos, is_top in goal_positions:
            goal_x = self.rink_x + (self.rink_width - self.goal_height) // 2
            
            # Draw goal frame
            pygame.draw.rect(self.screen, GameConstants.RED,
                           (goal_x, y_pos, self.goal_height, self.goal_depth), 
                           max(1, int(2 * self.scale)))
            
            # Draw net lines
            net_spacing = max(2, int(5 * self.scale))
            for i in range(net_spacing, self.goal_height, net_spacing):
                pygame.draw.line(self.screen, GameConstants.BLUE,
                               (goal_x + i, y_pos),
                               (goal_x + i, y_pos + self.goal_depth), 1)
            for j in range(net_spacing, self.goal_depth, net_spacing):
                pygame.draw.line(self.screen, GameConstants.BLUE,
                               (goal_x, y_pos + j),
                               (goal_x + self.goal_height, y_pos + j), 1)