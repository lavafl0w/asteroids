from circleshape import CircleShape, TriangleShape
from constants import (
    LINE_WIDTH,
    PLAYER_RADIUS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SHOT_COOLDOWN_SECONDS,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    PLAYER_HIT_COOLDOWN,
    SHIELD_RADIUS,
    SHIELD_MAX_HIT,
    SHIELD_ACTIVE_TIME,
    SHIELD_HIT_COOLDOWN
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
        self.active_shield = None

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
        
        # If a shield has been assigned    
        if self.active_shield is not None:
            self.active_shield.position = self.position # Update the position to player position
            if not self.active_shield.activated: # If shield has been removed
                self.active_shield = None # Remove link to player
        
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
        
        # Returns the channel so main.py can tell the player died    
        return death_channel
    
    # Add an effect to the player
    def player_effect_add(self, effect: str) -> None:
        
        # Add a shield if there is none
        if effect == "shield":
            if self.active_shield is None:
                self.active_shield = ShieldPowerup(self.position.x, self.position.y)
            else: # We already have a shield so refresh the values
                self.active_shield.refresh()

            
class ShieldPowerup(CircleShape):
    shield_activate_effect: pygame.mixer.Sound | None = None
    shield_deactivate_effect: pygame.mixer.Sound | None = None
    shield_hit_effect: pygame.mixer.Sound | None = None
    shield_break_effect: pygame.mixer.Sound | None = None
    
    def __init__(self, x, y) -> None:
        super().__init__(x, y, radius = SHIELD_RADIUS)
        self.activated = True
        self.shield_time_remaining = SHIELD_ACTIVE_TIME
        self.shield_hits_remaining = SHIELD_MAX_HIT
        self.shield_hit_cooldown = 0
        self.color = "orange"
        
        if self.shield_activate_effect is not None:
            self.shield_activate_effect.play()
        
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.color, self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        # Remove time remaining and cooldown of shield
        self.shield_time_remaining -= dt
        self.shield_hit_cooldown -= dt
        
        # If no more time available with the shield
        if self.shield_time_remaining <= 0:
            self.shield_deactivate()
            if self.shield_deactivate_effect is not None:
                self.shield_deactivate_effect.play()
            
        if self.shield_hit_cooldown > 0:
            self.color = "red"
        else:
            self.color = "orange"
    
    # Switch shield being activated and kills it        
    def shield_deactivate(self) -> None:
            self.activated = not self.activated
            self.kill()
        
    # Refresh shield values if picked up again
    def refresh(self) -> None:
        self.shield_hits_remaining = SHIELD_MAX_HIT
        self.shield_time_remaining = SHIELD_ACTIVE_TIME
        
    # Shield has been hit
    def hit(self) -> bool:
        # If shield is available
        if self.shield_hit_cooldown <= 0: 
            self.shield_hits_remaining -= 1 # Remove a hit
            
            # If that was the final hit
            if self.shield_hits_remaining == 0:
                self.shield_deactivate() # Deactivate it
                if self.shield_break_effect is not None:
                    self.shield_break_effect.play() # Play break sound
                    
                return True
            
            # It wasn't the final hit, so play hit sound
            if self.shield_hit_effect is not None:
                self.shield_hit_effect.play()
                
            # Set cooldown    
            self.shield_hit_cooldown = SHIELD_HIT_COOLDOWN    
            return True
        
        # Return false for no shield damage so main can call asteroid.bounce() instead
        return False
