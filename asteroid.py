from logger import log_event
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH

import pygame
import random


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
    
    # Draw circular asteroids
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)
    
    # On update: move the astroid    
    def update(self, dt: float) -> None:
        self.position += (self.velocity * dt)
    
    # Handles splitting of asteroids into smaller/fastrr ones when hit    
    def split(self) -> None:
        self.kill() # Regardless of size, this asteroid should be destroyed first
        
        # This was a small asteroid so do nothing
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        log_event("asteroid_split")
        new_rotation = random.uniform(20, 50)
        
        # Creates new rotation vectors for smaller asteroids
        new_velocity_1 = self.velocity.rotate(new_rotation)
        new_velocity_2 = self.velocity.rotate(-new_rotation)
        
        new_radius = self.radius - ASTEROID_MIN_RADIUS # Reduce radius
        
        # Create new asteroids at current position, use the new radius and apply velocity
        Asteroid(self.position.x, self.position.y, new_radius).velocity = new_velocity_1 * 1.2
        Asteroid(self.position.x, self.position.y, new_radius).velocity = new_velocity_2 * 1.2
        
