from circleshape import CircleShape, TriangleShape
from constants import (
    LINE_WIDTH,
    PLAYER_RADIUS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SHOT_COOLDOWN_SECONDS,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    PLAYER_HIT_COOLDOWN
)
from shot import Shot
import pygame
from scorekeeper import ScoreKeeper

class Player(CircleShape):    
    # All sounds get assigned after import
    death_audio: pygame.mixer.Sound | None = None
    shot_audio: pygame.mixer.Sound | None = None
    player_hit_audio: pygame.mixer.Sound | None = None
    
    def __init__(self, x: float, y:float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0
        self.hitbox_kind = "triangle"
        self.player_lives = 3
        self.color = "white"
        self.hit_cooldown = 0

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
        pygame.draw.polygon(screen, self.color, self.triangle(), 0)

    # Things to do every update() call
    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

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
        self.hit_cooldown -= dt # Decreases hit/invincible cooldown
        
        # If player is safe after last hit, they are red
        if self.hit_cooldown > 0:
            self.color = "red"
        else:
            self.color = "white"
        
    # Move back and forward
    def move(self, dt: float) -> None:
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
            bullet = Shot(self.position.x, self.position.y) # Create shot
            
            # Creates, rotates and increases speed of newly created shot
            bullet.velocity = pygame.math.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            
            if self.shot_audio is not None: # Pew pew pew
                self.shot_audio.play()
            
            self.shot_cooldown = PLAYER_SHOT_COOLDOWN_SECONDS # Set shot cooldown to max
            ScoreKeeper.shot_was_shot()
            
    def get_hitbox(self) -> TriangleShape:
        return self.triangle()
    
    def asteroid_hit(self) -> None | pygame.mixer.Channel:
        death_channel = None
        
        if self.hit_cooldown <= 0:
            if self.player_hit_audio is not None: # Oof
                self.player_hit_audio.play()
                
            if self.player_lives <= 1: # Death
                if self.death_audio is not None:
                    death_channel = self.death_audio.play()
                    
                self.hit_cooldown = PLAYER_HIT_COOLDOWN
                return death_channel
                
            # Remove life and reset cooldown
            self.player_lives -= 1
            self.hit_cooldown = PLAYER_HIT_COOLDOWN
            
        return death_channel

            
