import pygame
import sys

class Player:
    def __init__(self, screen, constants, rink_bounds):
        self.screen = screen
        self.constants = constants
        self.bounds = rink_bounds
        
        # Initialize position at center
        self.pos = pygame.math.Vector2(constants.BASE_WIDTH // 2, 
                                     constants.BASE_HEIGHT // 2)
        
        # NHL '94 style movement
        self.max_speed = 400
        self.acceleration = 2000
        self.deceleration = 1500
        self.turn_speed = 15
        
        self.velocity = pygame.math.Vector2()
        self.is_skating = False
        self.has_puck = False
        self.is_checking = False

    def move(self, dt):
        keys = pygame.key.get_pressed()
        
        # Get input direction
        direction = pygame.math.Vector2()
        if keys[pygame.K_w]: direction.y = -1
        if keys[pygame.K_s]: direction.y = 1
        if keys[pygame.K_a]: direction.x = -1
        if keys[pygame.K_d]: direction.x = 1
        
        # Normalize direction if moving diagonally
        if direction.length() > 0:
            direction = direction.normalize()
            self.is_skating = True
        else:
            self.is_skating = False
        
        # Apply acceleration/deceleration
        if self.is_skating:
            # Accelerate in input direction
            self.velocity += direction * self.acceleration * dt
            # Limit to max speed
            if self.velocity.length() > self.max_speed:
                self.velocity.scale_to_length(self.max_speed)
        else:
            # Decelerate when no input
            if self.velocity.length() > 0:
                decel_amount = self.deceleration * dt
                if self.velocity.length() <= decel_amount:
                    self.velocity = pygame.math.Vector2()
                else:
                    self.velocity -= self.velocity.normalize() * decel_amount
        
        # Update position
        self.pos += self.velocity * dt
        
        # Bouncing off boards
        if self.pos.x < self.bounds['left']:
            self.pos.x = self.bounds['left']
            self.velocity.x *= -0.5
        elif self.pos.x > self.bounds['right']:
            self.pos.x = self.bounds['right']
            self.velocity.x *= -0.5
            
        if self.pos.y < self.bounds['top']:
            self.pos.y = self.bounds['top']
            self.velocity.y *= -0.5
        elif self.pos.y > self.bounds['bottom']:
            self.pos.y = self.bounds['bottom']
            self.velocity.y *= -0.5
    
    def draw(self):
        # Draw player shadow
        shadow_pos = self.pos + pygame.math.Vector2(2, 2)
        pygame.draw.circle(self.screen, (30, 30, 30), shadow_pos, 12)
        
        # Draw player
        color = (255, 0, 0) if self.has_puck else (0, 0, 255)
        pygame.draw.circle(self.screen, color, self.pos, 12)
        
        # Draw direction indicator
        if self.velocity.length() > 0:
            direction = self.velocity.normalize()
            indicator_pos = self.pos + direction * 15
            pygame.draw.circle(self.screen, (255, 255, 255), indicator_pos, 3)