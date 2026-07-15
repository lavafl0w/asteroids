import pygame
from circleshape import CircleShape
from constants import BOMB_DETONATE_TIME, TIME_UNTIL_ITEM_DESPAWN, MAX_BOMB_EXPLOSION_TIME, LINE_WIDTH
from logger import log_event
from scorekeeper import ScoreKeeper

# PARENT ITEM CLASS #
class ItemPickup(CircleShape):
    def __init__(self, x:float, y:float) -> None:
        super().__init__(x, y, radius = 0)
        self.time_until_despawn = TIME_UNTIL_ITEM_DESPAWN
        self.activated = False
        self.flash_timer = 0.0
        self.color = "white"
        self.visible = True
        self.hitbox_kind = "rect"
    
    # Helper for if item has been activated    
    def activate(self) -> bool:
        if self.activated:
            return False # It's already been activated
        self.activated = True
        ScoreKeeper.item_was_picked_up()
        return True
    
    # Helper for changing the color of the item and starts it flashing    
    def update_warning_flash(self, dt: float, color: str) -> None:
        self.color = color
        self.flash_timer += dt
         
        # Flash faster as the bomb gets closer to despawning.
        flash_interval = max(0.1, self.time_until_despawn / 10)
        if self.flash_timer >= flash_interval:
            self.visible = not self.visible
            self.flash_timer = 0.0
    
    # Logic for the item still being able to despawn        
    def item_to_despawn(self, dt: float) -> None:
        self.time_until_despawn -= dt # Remove time left

        # Times up!
        if self.time_until_despawn <= 0:
            self.kill() # Delete it
            return

        # There is still double the time left to pick it up
        if self.time_until_despawn > (TIME_UNTIL_ITEM_DESPAWN/2):
            self.color = "white"
            self.visible = True
            self.flash_timer = 0.0
            return

        # Getting closer, it's gonna despawn!
        self.update_warning_flash(dt, "yellow")
        
    def item_rect(self) -> pygame.Rect:
        raise NotImplementedError(f"{self.__class__.__name__} hasn't implemented an item_rect method")
        
    def hitbox_shape(self) -> pygame.Rect:
        return self.item_rect()

class Bomb(ItemPickup):
    explosion_sound: pygame.mixer.Sound | None = None # Start bomb with no sound effect until after mixer is initialised
    width = 40
    height = 25
    
    def __init__(self, x:float, y:float) -> None:
        super().__init__(x, y)
        self.detonate_timer = BOMB_DETONATE_TIME
        
    def item_rect(self) -> pygame.Rect:        
        bomb = pygame.Rect(0, 0, self.width, self.height)
        bomb.center = (int(self.position.x), int(self.position.y))
        return bomb
        
    def draw(self, screen: pygame.Surface) -> None:
        if self.visible:
            pygame.draw.rect(screen, self.color, self.item_rect())
    
    # Call general activate function and set despawn time to 3
    def activate(self) -> bool:
        if super().activate(): # Bomb got activated 
            ScoreKeeper.bomb_was_activated()
            self.time_until_despawn = 3 # This is so the bomb flashes faster when activated
            return True
        return False

    def update(self, dt: float) -> None:
        # Item hasn't been activated yet
        if self.activated == False: 
            super().item_to_despawn(dt) # Call despawn logic
                    
        # Activated so let's blow something up!
        elif self.activated == True: 
            # Beep-Beep-Beep
            if self.detonate_timer > 0:
                self.update_warning_flash(dt, "red")
                self.detonate_timer -= dt
                return
            
            # Boom
            self.detonate()
    
    # How to boom        
    def detonate(self) -> None:
        log_event("bomb_detonated")
        if Bomb.explosion_sound is not None: # If the sound has been attached
            Bomb.explosion_sound.play() # Make important boom noise
        self.kill() # Remove bomb cause it went boom
        BombExplosion(self.position.x, self.position.y, 1) # Start bomb explosion from where bomb was
        
# This handles creating the expanding explosion radius
class BombExplosion(CircleShape):
    def __init__(self, x:float, y:float, radius:float, time_left:float = MAX_BOMB_EXPLOSION_TIME) -> None:
        super().__init__(x, y, radius)
        self.time_left = time_left # How long the explosion has left to explode
        
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "red", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.time_left -= dt # Decrease how long the explosion has left
        
        # If the explosion hasn't finished yet then
        if self.time_left > 0:
            # Make a new radius with basically the same params, but increase radius and pass in the remaining
            # amount of time the explosion has left
            BombExplosion(self.position.x, self.position.y, self.radius + 1, self.time_left)    
        
        self.kill() # Kill this instance
