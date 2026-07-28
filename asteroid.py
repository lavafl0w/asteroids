from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from powerups import check_powerup_drop
from scorekeeper import ScoreKeeper
import pygame
import random

#! Currently only uses circle collision logic instead of actual shape collision
class Asteroid(CircleShape):
    asteroid_split_sound: pygame.mixer.Sound | None = None  # Asteroid split sound gets assigned after importing
    
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.local_point_coords: list[pygame.Vector2] = self.create_local_polygon_coords() # Create local polygon points for drawing
    
    # Draw circular asteroids
    def draw(self, screen: pygame.Surface) -> None:
        world_point_coords = [self.position + point for point in self.local_point_coords]        
        pygame.draw.polygon(screen, "white", world_point_coords, LINE_WIDTH)
    
    # On update: move the astroid    
    def update(self, dt: float) -> None:
        self.position += (self.velocity * dt)
        # TODO: Replace this magic boundary with one based on screen size and asteroid radius.
        if abs(self.position.x) > 2000 or abs(self.position.y) > 2000:
            self.kill() # Remove asteroid if it's far outside screen boundaries
    
    # Handles splitting of asteroids into smaller/faster ones when hit    
    def split(self) -> None:
        self.kill() # Regardless of size, destroy it
        
        if Asteroid.asteroid_split_sound is not None:
            Asteroid.asteroid_split_sound.play()
        
        # This was a small asteroid
        if self.radius <= ASTEROID_MIN_RADIUS:
            ScoreKeeper.asteroid_was_shot()
            
            #// NOTE: This is where the powerup drop logic will live
            # NOTE: Powerup drop logic now lives in powerups.py
            check_powerup_drop(self.position)           

            return

        new_rotation = random.uniform(20, 50)
        
        # Creates new rotation vectors for smaller asteroids
        new_velocity_1 = self.velocity.rotate(new_rotation)
        new_velocity_2 = self.velocity.rotate(-new_rotation)
        
        new_radius = self.radius - ASTEROID_MIN_RADIUS # Reduce radius
        
        # Create new asteroids at current position, use the new radius and apply velocity
        Asteroid(self.position.x, self.position.y, new_radius).velocity = new_velocity_1 * 1.2
        Asteroid(self.position.x, self.position.y, new_radius).velocity = new_velocity_2 * 1.2
    
    # Handles bouncing the direction of the asteroid away   
    def bounce(self, bounce_object: CircleShape) -> None:
        # Gets a vector (normal) that points away from other object
        push_direction_vector = self.position - bounce_object.position
        
        # Gets the distance and gets the overlap amount
        centre_distance = self.position.distance_to(bounce_object.position)
        overlap = (bounce_object.radius + self.radius) - centre_distance
        
        
        # Make the new position a spot away from the other object
        # in the other direction
        # TODO: Guard against zero-length vectors before normalizing.
        # TODO: Asteroid/asteroid bounce currently only moves this asteroid, not both.
        self.position += push_direction_vector.normalize() * overlap
    
    # TODO: Sort out comments and variable names    
    def create_local_polygon_coords(self) -> list[pygame.Vector2]:
        # FUTURE: Start with large, but have different no. of segments depending of size(maybe radius?)
        '''
        This will be the function that creates the list of local coordinates for each point around the asteroid
        This is then stored, so the random variation doesn't change for each draw cycle.
        
        Asteroid is split into segments, with each segement a random local coordinate from centre
        Asteroid position (centre) -> Vector out at an angle with length of radius (plus small randomness)
        Points are then drawn in relation asteroid centre using world coordinate system
        '''
        # Asteroid is split into 30 degree chunks for 12 coordinates
        '''
        0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, (not 360 as this is also 0), centre is 0,0
        '''
        
        segement_degree_step = 20
        local_coordinates_30_degree_12p: list[pygame.Vector2] = []
        
        min_random = 0.85
        max_random = 1.12
        
        random_factor = random.uniform(min_random, max_random) # Lets say this is 0.9
        max_random_range = 0.15
        
        for segement_degree in range(0, 360, segement_degree_step):
            
            new_factor = random.uniform(min_random, max_random) # This is 1.1 - We want to bring this down to 0.98
            # TODO: This clamps to the global min/max, not to the previous factor +/- max_random_range.
            if abs(new_factor - random_factor) > max_random_range:
                new_factor = min(max_random, max(new_factor, min_random))
            
            random_factor = new_factor
            
            base_vector = pygame.Vector2(1, 0) # Vector pointing right (eg angle 0)
            distance_value = self.radius * random_factor
            scaled_vector = base_vector * distance_value
            segement_coord = scaled_vector.rotate(segement_degree)
            
            local_coordinates_30_degree_12p.append(segement_coord)
        
        return local_coordinates_30_degree_12p
