import pygame

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...] # type: ignore

    def __init__(self, x: float, y: float, radius: float) -> None:
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(*self.containers) # type: ignore
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
    
    # Collision logic
    def collides_with(self, other: "CircleShape") -> bool:
        # Calculate distance between center of each CircleShape object
        center_distances = pygame.math.Vector2.distance_to(self.position, other.position)
        
        # When distance between center points is the same or less than both radius's put together --- return true
        if center_distances <= (self.radius + other.radius):
            return True
        
        return False