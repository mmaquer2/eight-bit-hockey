import pygame
import sys

class Player:
    def __init__(self, window, start_x, start_y):
        self.screen = window
        self.pos = pygame.math.Vector2(start_x, start_y)  # Use passed in starting position
        self.direction = pygame.math.Vector2()
        self.speed = 300  # Pixels per second
        
    def input(self):
        keys = pygame.key.get_pressed()
        
        # Reset direction each frame
        self.direction.x = 0
        self.direction.y = 0
        
        # WASD movement 
        if keys[pygame.K_w]:
            print("W pressed")
            self.direction.y = -1
        if keys[pygame.K_s]:
            self.direction.y = 1
        if keys[pygame.K_a]:
            self.direction.x = -1
        if keys[pygame.K_d]:
            self.direction.x = 1
            
        # Normalize diagonal movement to prevent faster diagonal speed
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
    
    def move(self, dt):
        # Move based on direction and delta time
        self.pos += self.direction * self.speed * dt
        
        # Optional: Add screen boundary checking
        screen_rect = self.screen.get_rect()
        self.pos.x = max(10, min(self.pos.x, screen_rect.width - 10))
        self.pos.y = max(10, min(self.pos.y, screen_rect.height - 10))
    
    def update(self, dt):
        self.input()
        self.move(dt)
    
    def draw(self):
        pygame.draw.circle(self.screen, "purple", self.pos, 10)