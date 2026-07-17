import pygame

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]
    hitbox_kind = "circle"

    def __init__(self, x: float, y: float, radius: float) -> None:
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()

        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius


    def draw(self, screen: pygame.Surface) -> None:
        # must override
        pass

    def update(self, dt: float) -> None:
        # must override
        pass
        
    def get_hitbox(self) -> "HitboxShape":
        return self
    
TriangleShape = tuple[pygame.Vector2, pygame.Vector2, pygame.Vector2]
HitboxShape = CircleShape | pygame.Rect | TriangleShape
