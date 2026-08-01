import pygame
from base import BaseItemPowerup
from player import Player
from constants import SHIELD_ITEM_PICKUP_RADIUS, HEALTH_PICKUP_RADIUS

# Shield powerup on screen
class ShieldPowerupItem(BaseItemPowerup):    
    hitbox_kind = "circle"
    color = "orange"
    
    def __init__(self, x, y) -> None:
        super().__init__(x, y, SHIELD_ITEM_PICKUP_RADIUS)
      
    def draw(self, screen: pygame.Surface) -> None:
        if self.is_visible: # Needed for flashing despawn
            pygame.draw.circle(screen, self.color, self.position, self.radius, 0)

    def update(self, dt: float) -> None:
        if not self.is_activated: # It's not been picked up
            super().handle_despawn(dt)
    
    def activate(self, player: Player | None = None) -> bool | None:
        if player: # Needed just cause player might also be None
            player.player_effect_add("shield") # Call function from Player class
            super().activate() # Deal with main activation
            self.kill() # Remove from screen

# Health/extra life            
class HealthPickup(BaseItemPowerup):
    hitbox_kind = "circle"
    color = "green"
    
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, HEALTH_PICKUP_RADIUS)
            
    # Creates two Rects, centres them then draws both intersecting as a cross
    def draw(self, screen: pygame.Surface) -> None:
        if self.is_visible:
            horizontal_rect = pygame.Rect(0,0,15,5)
            vertical_rect = pygame.Rect(0,0,5,15)
            
            horizontal_rect.center = (int(self.position.x), int(self.position.y))
            vertical_rect.center = (int(self.position.x), int(self.position.y))
            
            pygame.draw.rect(screen, self.color, horizontal_rect)
            pygame.draw.rect(screen, self.color, vertical_rect)
    
    # Despawn logic
    def update(self, dt:float) -> None:
        if not self.is_activated: 
            super().handle_despawn(dt)
            
    # Call player effect method to add life before removing itself
    def activate(self, player: Player | None = None) -> bool | None:
        if player: # Needed just cause player might also be None
            player.player_effect_add("health") # Call function from Player class
            super().activate() # Deal with main activation
            self.kill() # Remove from screen