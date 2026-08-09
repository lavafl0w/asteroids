import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]
    hitbox_kind = "circle"

    def __init__(self, x: float, y: float, radius: float) -> None:
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()

        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.screen_boundary_margin = self.radius * 5

    def draw(self, screen: pygame.Surface) -> None:
        pass

    def update(self, dt: float) -> None:
        pass
    
    # Returns assigned hitbox for shape for collison detection    
    def get_hitbox(self) -> "HitboxShape":
        return self
    
    # Checks if object has moved off screen and flips position
    def wrap_position(self) -> None:
        if self.position.x - self.radius > SCREEN_WIDTH:
            self.position.x = -self.radius
        elif self.position.x + self.radius < 0:
            self.position.x = SCREEN_WIDTH + self.radius
            
        if self.position.y - self.radius > SCREEN_HEIGHT:
            self.position.y = -self.radius
        elif self.position.y + self.radius < 0:
            self.position.y = SCREEN_HEIGHT + self.radius
    
TriangleShape = tuple[pygame.Vector2, pygame.Vector2, pygame.Vector2]
HitboxShape = CircleShape | pygame.Rect | TriangleShape
