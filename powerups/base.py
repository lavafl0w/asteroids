import pygame
from circle_shape import CircleShape
from score_keeper import ScoreKeeper
from player import Player
from constants import TIME_LEFT_BEFORE_ITEM_DESPAWN

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
    def activate(self, player: Player | None = None) -> bool | None:
        if self.is_activated:
            return False # It's already been activated, so it didn't get activated again
        self.is_activated = True
        ScoreKeeper.item_was_picked_up()
        return True # Item was activated
    
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