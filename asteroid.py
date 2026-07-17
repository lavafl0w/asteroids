from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH, BOMB_SPAWN_CHANCE
from powerups import Bomb, ShieldPowerupItem
from scorekeeper import ScoreKeeper
import pygame
import random


class Asteroid(CircleShape):
    asteroid_split_sound: pygame.mixer.Sound | None = None # Asteroid split sound gets assigned after importing
    
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
    
    # Draw circular asteroids
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)
    
    # On update: move the astroid    
    def update(self, dt: float) -> None:
        self.position += (self.velocity * dt)
    
    # Handles splitting of asteroids into smaller/faster ones when hit    
    def split(self) -> None:
        self.kill() # Regardless of size, this asteroid should be destroyed first
        
        if Asteroid.asteroid_split_sound is not None: # Check sound is assigned and play
            Asteroid.asteroid_split_sound.play()
        
        # This was a small asteroid
        if self.radius <= ASTEROID_MIN_RADIUS:
            ScoreKeeper.asteroid_was_shot()
            # NOTE: This is where the powerup logic will live
            if random.randrange(0, 100) < BOMB_SPAWN_CHANCE: # If this should be a bomb
                ShieldPowerupItem(self.position.x, self.position.y)
                #Bomb(self.position.x, self.position.y)
                return # Return after so multiple powerups don't spawn
            
            return

        new_rotation = random.uniform(20, 50)
        
        # Creates new rotation vectors for smaller asteroids
        new_velocity_1 = self.velocity.rotate(new_rotation)
        new_velocity_2 = self.velocity.rotate(-new_rotation)
        
        new_radius = self.radius - ASTEROID_MIN_RADIUS # Reduce radius
        
        # Create new asteroids at current position, use the new radius and apply velocity
        Asteroid(self.position.x, self.position.y, new_radius).velocity = new_velocity_1 * 1.2
        Asteroid(self.position.x, self.position.y, new_radius).velocity = new_velocity_2 * 1.2
        
