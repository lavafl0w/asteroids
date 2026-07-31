from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT
from powerups import check_powerup_drop
from scorekeeper import ScoreKeeper
import debug_flags
import pygame
import random

#! Currently only uses circle collision logic instead of actual shape collision
class Asteroid(CircleShape):
    asteroid_split_sound: pygame.mixer.Sound | None = None  # Asteroid split sound gets assigned after importing
    
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.local_point_coords: list[pygame.Vector2] = self.create_local_polygon_coords() # Create local polygon points for drawing
        self.color = "white"

    def draw(self, screen: pygame.Surface) -> None:
        if debug_flags.check("DEBUG_ASTEROID_POLYGON_OUTLIERS"): #!
            self.debug_polygon_outliers()

        world_point_coords = [self.position + point for point in self.local_point_coords]
        pygame.draw.polygon(screen, self.color, world_point_coords, LINE_WIDTH)

    def debug_polygon_outliers(self) -> None: #!
        """Print if a local polygon point is suspiciously far from this asteroid."""
        max_expected_distance = self.radius * 2

        for index, local_point in enumerate(self.local_point_coords):
            point_distance = local_point.length()

            if point_distance > max_expected_distance:
                print(
                    "asteroid polygon outlier -> "
                    f"center={self.position}, radius={self.radius}, "
                    f"point_index={index}, local_point={local_point}, "
                    f"distance_from_center={point_distance}"
                )
 
    def update(self, dt: float) -> None:
        self.position += (self.velocity * dt)
                    
        if (    # Remove asteroid if it's far outside screen boundaries
            self.position.x < -self.screen_boundary_margin
            or self.position.y < -self.screen_boundary_margin
            or self.position.x > SCREEN_WIDTH + self.screen_boundary_margin
            or self.position.y > SCREEN_HEIGHT + self.screen_boundary_margin
        ):  
            self.kill() 

    def split(self) -> None:
        """Handles splitting of asteroids into smaller/faster ones when hit"""
        self.kill() # Regardless of size, destroy it
        
        if Asteroid.asteroid_split_sound is not None:
            Asteroid.asteroid_split_sound.play()
        
        # This was a small asteroid
        if self.radius <= ASTEROID_MIN_RADIUS:
            ScoreKeeper.asteroid_was_shot()
            check_powerup_drop(self.position) # Roll for a possible powerup
            return

        new_rotation = random.uniform(20, 50)
        
        # Creates new rotation vectors for smaller asteroids
        new_velocity_1 = self.velocity.rotate(new_rotation)
        new_velocity_2 = self.velocity.rotate(-new_rotation)
        
        new_radius = self.radius - ASTEROID_MIN_RADIUS # Reduce radius
        
        # Create new asteroids at current position, use the new radius and apply velocity
        Asteroid(self.position.x, self.position.y, new_radius).velocity = new_velocity_1 * 1.2
        Asteroid(self.position.x, self.position.y, new_radius).velocity = new_velocity_2 * 1.2

    def bounce(self, bounce_object: CircleShape) -> None:
        """Handles bouncing the direction of the asteroid away"""
        #TODO: This 'bouncing' is more like 'sliding around' each other rn lol
        # Gets a vector (normal) that points away from other object
        push_direction_vector = self.position - bounce_object.position
        
        # Gets the distance and gets the overlap amount
        centre_distance = self.position.distance_to(bounce_object.position)
        overlap = (bounce_object.radius + self.radius) - centre_distance
        
        if debug_flags.check("DEBUG_ASTEROID_OVERLAP_CHECK"):#!
            if overlap > self.radius*2: 
                print(
                        "asteroid overlap -> "
                        f"center={self.position}, radius={self.radius}, "
                        f"overlap={overlap}, distance={centre_distance}, "
                        f"other center={bounce_object.position}, other radius={bounce_object.radius}"
                    )
        
        # Guard against zero-length vectors before normalizing.
        if push_direction_vector.length() == 0:
            push_direction_vector = pygame.Vector2(1,0)
        push_direction_vector.normalize_ip()
        
        # TODO: Look at asteroid vs shield, since now both objects move but shield shouldn't without HACK
        # HACK: If its an asteroid, split the overlap then move both
        if isinstance(bounce_object, Asteroid):
            overlap /= 2
            bounce_object.position -= push_direction_vector * overlap
            
        # Make the new position a spot away from the other object
        self.position += push_direction_vector * overlap
        
    def create_local_polygon_coords(self) -> list[pygame.Vector2]:
        """Creates a list of randomly positioned coordinates for drawing a 'rocky' asteroid shape."""
        #FUTURE: Have different no. of segments depending on size(maybe radius?)
        
        # Asteroid is split into 20 degree chunks
        segement_degree_step = 20
        local_coords: list[pygame.Vector2] = []
        
        min_rand_limit = 0.85
        max_rand_limit = 1.12
        
        #FUTURE: Clean up double upper/lower range calcs here and in for loop
        random_factor = random.uniform(min_rand_limit, max_rand_limit)
        rand_factor_range = 0.15 # How much the different factors can deviate from each other
        upper_range = random_factor + rand_factor_range
        lower_range = random_factor - rand_factor_range
        
        for segement_degree in range(0, 360, segement_degree_step):
            new_factor = random.uniform(min_rand_limit, max_rand_limit)

            if abs(new_factor - random_factor) > rand_factor_range: # If new factor deviates to much, clamp it
                new_factor = min(upper_range, max(new_factor, lower_range))
            
            # Store this value for next run, calculate new range
            #FUTURE: currently, initial factor on first loop doesn't actually get used
            random_factor = new_factor
            upper_range = random_factor + rand_factor_range
            lower_range = random_factor - rand_factor_range
            
            base_vector = pygame.Vector2(1, 0) # Vector pointing right (eg angle 0)
            distance_value = self.radius * random_factor # Work out length for vector
            
            scaled_vector = base_vector * distance_value # Combine the length with vector
            segement_coord = scaled_vector.rotate(segement_degree) # Point it towards angle
            
            local_coords.append(segement_coord)
        
        return local_coords