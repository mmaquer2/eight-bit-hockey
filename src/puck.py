import pygame

class Puck:
    def __init__(self, screen, constants, rink_bounds):
        self.screen = screen
        self.constants = constants
        self.bounds = rink_bounds
        self.pos = pygame.math.Vector2(constants.BASE_WIDTH // 2, 
                                     constants.BASE_HEIGHT // 2)
        self.velocity = pygame.math.Vector2()
        
        # Puck physics
        self.friction = 0.98  # Ice friction
        self.bounce = 0.7    # Board bounce factor
        
    def update(self, dt):
        # Apply friction
        self.velocity *= self.friction
        
        # Update position
        self.pos += self.velocity * dt
        
        # Bounce off boards
        if self.pos.x < self.bounds['left']:
            self.pos.x = self.bounds['left']
            self.velocity.x *= -self.bounce
        elif self.pos.x > self.bounds['right']:
            self.pos.x = self.bounds['right']
            self.velocity.x *= -self.bounce
            
        if self.pos.y < self.bounds['top']:
            self.pos.y = self.bounds['top']
            self.velocity.y *= -self.bounce
        elif self.pos.y > self.bounds['bottom']:
            self.pos.y = self.bounds['bottom']
            self.velocity.y *= -self.bounce
    
    def draw(self):
        # Draw puck shadow
        shadow_pos = self.pos + pygame.math.Vector2(1, 1)
        pygame.draw.circle(self.screen, (30, 30, 30), shadow_pos, 6)
        
        # Draw puck
        pygame.draw.circle(self.screen, (0, 0, 0), self.pos, 6)