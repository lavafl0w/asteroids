import pygame
from circleshape import CircleShape
from constants import (
    BOMB_DETONATE_COUNTDOWN_TIME,
    TIME_LEFT_BEFORE_ITEM_DESPAWN,
    MAX_BOMB_EXPLOSION_TIME,
    LINE_WIDTH,
    BOMB_EXPLOSION_RADIUS_EXPANSION,
    SHIELD_ITEM_PICKUP_RADIUS, 
    ITEM_WIDTH,
    ITEM_HEIGHT
)
from scorekeeper import ScoreKeeper
from player import Player

# PARENT ITEM CLASS #
class BaseItemPowerup(CircleShape):
    color = "white"
    
    def __init__(self, x:float, y:float, radius:float = 0) -> None:
        super().__init__(x, y, radius)
        self.time_until_despawn = TIME_LEFT_BEFORE_ITEM_DESPAWN
        self.is_activated = False
        self.time_between_blinks = 0.0
        self.is_visible = True
    
    # Helper for if item has been activated    
    def activate(self, player: Player | None = None) -> bool:
        if self.is_activated:
            return False # It's already been activated
        self.is_activated = True
        ScoreKeeper.item_was_picked_up()
        return True
    
    # Helper for changing the color of the item and starts it flashing    
    def update_warning_blink(self, dt: float) -> None:
        self.time_between_blinks += dt
         
        # Blink more and more quickly as the time left before despawning gets lower.
        blink_interval = max(0.1, self.time_until_despawn / 10)
        if self.time_between_blinks >= blink_interval:
            self.is_visible = not self.is_visible
            self.time_between_blinks = 0.0
    
    # What the item should look like while still on screen        
    def handle_despawn(self, dt: float) -> None:
        self.time_until_despawn -= dt # Remove time available

        # Times up!
        if self.time_until_despawn <= 0:
            self.kill() # Delete it
            return

        # There is still double the time left to pick it up
        if self.time_until_despawn >= (TIME_LEFT_BEFORE_ITEM_DESPAWN/2):
            self.is_visible = True
            self.time_between_blinks = 0.0
            return

        # Getting closer, it's gonna go!
        self.update_warning_blink(dt)
        
    def get_item_shape(self) -> pygame.Rect:
        raise NotImplementedError(f"{self.__class__.__name__} hasn't implemented an item_rect method")
        
    def get_hitbox(self) -> pygame.Rect | CircleShape:
        if self.hitbox_kind == "rect":
            return self.get_item_shape()
        return self

class Bomb(BaseItemPowerup):
    explosion_sound: pygame.mixer.Sound | None = None # Sound effects set at None for import, attached after
    countdown_sound: pygame.mixer.Sound | None = None
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
    def activate(self, player: Player | None = None) -> bool:
        if super().activate(): # Bomb got activated 
            ScoreKeeper.bomb_was_activated()
            self.color = "red"
            self.time_until_despawn = self.time_before_detonation # This is so the bomb flashes faster on trigger
            if Bomb.countdown_sound is not None: # Play the first beep as it doesn't look right without it
                Bomb.countdown_sound.play()
            return True
        return False

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
                # If the bomb sound exists, and the bomb has flashed off -> on this frame
                if Bomb.countdown_sound is not None and (not old_visible_state and self.is_visible):
                    Bomb.countdown_sound.play()
               
                self.time_before_detonation -= dt
                return
            
            # Boom
            self.detonate()
    
    # How to boom        
    def detonate(self) -> None:
        if Bomb.explosion_sound is not None: # If the sound has been attached
            Bomb.explosion_sound.play() # Make important boom noise
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

# Shield powerup on screen
class ShieldPowerupItem(BaseItemPowerup):    
    hitbox_kind = "circle"
    color = "orange"
    
    def __init__(self, x, y) -> None:
        super().__init__(x, y, SHIELD_ITEM_PICKUP_RADIUS)
      
    def draw(self, screen: pygame.Surface) -> None:
        if self.is_visible:
            pygame.draw.circle(screen, self.color, self.position, self.radius, 0)

    def update(self, dt: float) -> None:
        if not self.is_activated:
            super().handle_despawn(dt)
    
    def activate(self, player: Player | None = None) -> bool:
        if player:
            player.player_effect_add("shield")
            super().activate()
            self.kill()
            return True
        return False