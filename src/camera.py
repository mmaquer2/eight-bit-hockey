import pygame

class Camera:
    def __init__(self, game_constants):
        self.constants = game_constants
        self.zoom = 1.0
        self.min_zoom = 0.5  # Show more of the rink
        self.max_zoom = 2.0  # Get closer to action
        self.zoom_speed = 0.1
        self.offset = pygame.math.Vector2(0, 0)
        
    def apply_zoom(self, surface, pos):
        """Convert world position to screen position with zoom"""
        zoomed_pos = pygame.math.Vector2(pos) * self.zoom - self.offset
        return zoomed_pos
    
    def reverse_zoom(self, screen_pos):
        """Convert screen position to world position"""
        return (pygame.math.Vector2(screen_pos) + self.offset) / self.zoom
    
    def adjust_zoom(self, amount):
        """Change zoom level while keeping it within bounds"""
        proposed_zoom = self.zoom + amount * self.zoom_speed
        self.zoom = max(self.min_zoom, min(proposed_zoom, self.max_zoom))

    def follow(self, target_pos):
        """Make camera follow a target (like the puck or active player)"""
        screen_center = pygame.math.Vector2(self.constants.BASE_WIDTH // 2, 
                                          self.constants.BASE_HEIGHT // 2)
        target = pygame.math.Vector2(target_pos)
        self.offset = (target * self.zoom) - screen_center

    def update(self, dt):
        """Update camera smoothly"""
        pass