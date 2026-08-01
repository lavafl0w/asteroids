import pygame
from core.audio_manager import audio
from score_keeper import ScoreKeeper
from base import BaseItemPowerup
from constants import (BOMB_DETONATE_COUNTDOWN_TIME, ITEM_WIDTH, 
                       ITEM_HEIGHT, MAX_BOMB_EXPLOSION_TIME, LINE_WIDTH,
                       BOMB_EXPLOSION_RADIUS_EXPANSION)
from player import Player
from circle_shape import CircleShape

class Bomb(BaseItemPowerup):
    width = ITEM_WIDTH
    height = ITEM_HEIGHT
    hitbox_kind = "rect"
    
    def __init__(self, x:float, y:float) -> None:
        super().__init__(x, y)
        self.color = "blue"
        self.time_before_detonation = BOMB_DETONATE_COUNTDOWN_TIME
        
    def get_item_shape(self) -> pygame.Rect:        
        bomb_rect = pygame.Rect(0, 0, self.width, self.height)
        bomb_rect.center = (int(self.position.x), int(self.position.y))
        return bomb_rect
        
    def draw(self, screen: pygame.Surface) -> None:
        if self.is_visible: # default = True
            pygame.draw.rect(screen, self.color, self.get_item_shape())
    
    # Call parent activate function and set despawn time to 3
    def activate(self, player: Player | None = None) -> bool | None:
        if super().activate(): # Bomb got activated 
            ScoreKeeper.bomb_was_activated()
            self.color = "red"
            self.time_until_despawn = self.time_before_detonation # This is so the bomb flashes faster on trigger
            audio.play_effect(audio.bomb_countdown_sound) # Play the first beep as it doesn't look right without it

    def update(self, dt: float) -> None:
        # Item hasn't been activated yet
        if not self.is_activated: 
            super().handle_despawn(dt) # Call despawn logic
                    
        # Activated so let's blow something up!
        elif self.is_activated == True: 
            # Beep-Beep-Beep
            if self.time_before_detonation > 0:
                old_visible_state = self.is_visible
                self.update_warning_blink(dt)
                
                # If the bomb has flashed off -> on this frame
                if (not old_visible_state and self.is_visible):
                    audio.play_effect(audio.bomb_countdown_sound) # Beep
               
                self.time_before_detonation -= dt
                return
            
            # Boom
            self.detonate()
    
    # How to boom        
    def detonate(self) -> None:
        audio.play_effect(audio.bomb_explosion_sound) # Make important boom noise
        self.kill() # Remove bomb cause it went boom
        BombExplosion(self.position.x, self.position.y, 1) # Start bomb explosion from where bomb was, radius 1
        
# This handles creating the expanding explosion radius
class BombExplosion(CircleShape):
    def __init__(self, x:float, y:float, radius:float, explosion_time_left:float = MAX_BOMB_EXPLOSION_TIME) -> None:
        super().__init__(x, y, radius)
        self.explosion_time_left = explosion_time_left # How long the explosion has left to explode
        
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "red", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.explosion_time_left -= dt # Decrease how long the explosion has left
        
        # If the explosion still has time
        if self.explosion_time_left > 0:
            # Make a new explosion radius with basically the same params, but increase radius and pass in the remaining
            # amount of time the explosion has left
            BombExplosion(self.position.x, self.position.y, self.radius + BOMB_EXPLOSION_RADIUS_EXPANSION, self.explosion_time_left)    
        
        self.kill() # Kill this instance