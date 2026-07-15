from circleshape import CircleShape, TriangleShape
from constants import (
    LINE_WIDTH,
    PLAYER_RADIUS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SHOT_COOLDOWN_SECONDS,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
)
from shot import Shot
import pygame
from scorekeeper import ScoreKeeper

class Player(CircleShape):
    def __init__(self, x: float, y:float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0
        self.hitbox_kind = "triangle"
        # Possible extension point: temporary player effects can live alongside the usual player state.

    # Simply create triangle points
    def triangle(self) -> TriangleShape:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        nose = self.position + forward * self.radius
        back_right = self.position - forward * self.radius - right
        back_left = self.position - forward * self.radius + right
        return (nose, back_left, back_right)

    # Draw a triangle on the screen, coloured white with a line width from constants
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    # Things to do every update() call
    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        # Note: Future powerup hook: timed effects can be maintained as part of the normal frame update.

        if keys[pygame.K_w]: # Move forward - Key: W
            self.move(dt)
        if keys[pygame.K_a]: # Rotates left - Key: A
            self.rotate(-dt)
        if keys[pygame.K_s]: # Move backward - Key : S
            self.move(-dt)
        if keys[pygame.K_d]: # Rotates right - Key: D
            self.rotate(dt)
        if keys[pygame.K_SPACE]: # Shoot - Key: Space
            self.shoot()
            
            
        self.shot_cooldown -= dt # Decreases shot cooldown
        
    # Move back and forward
    def move(self, dt: float) -> None:
        # Possible extension point: movement is a natural place for temporary speed-related effects.
        unit_vector = pygame.math.Vector2(0,1) # Creates a unit vector of length 1
        rotated_vector = unit_vector.rotate(self.rotation) # Rotates vector in same direction of player
        speed_vector = rotated_vector * PLAYER_SPEED * dt # Extends the length of the vector by how much the player should move in frame
        self.position += speed_vector # Makes this the new position
        
    # Rotates player sprite
    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt
    
    # Shoot a shot
    def shoot(self) -> None:
        
        if self.shot_cooldown <= 0:
            
            # Create shot
            bullet = Shot(self.position.x, self.position.y) 
            # Creates, rotates and increases speed of newly created shot
            bullet.velocity = pygame.math.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            # Pew pew pew
            pygame.mixer.Sound("assets/pew-pew-lame-sound-effect.mp3").play()
            # Set shot cooldown to max
            self.shot_cooldown = PLAYER_SHOT_COOLDOWN_SECONDS
            ScoreKeeper.shot_was_shot()
            
    def hitbox_shape(self) -> TriangleShape:
        return self.triangle()
            
