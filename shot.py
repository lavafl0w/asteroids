from circleshape import CircleShape
from constants import SHOT_RADIUS, LINE_WIDTH
import pygame

class Shot(CircleShape):
    def __init__(self, x: float, y:float) -> None:
        super().__init__(x, y, SHOT_RADIUS)
        
    # Draw circular bullets
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, 0)
    
    # On update: move the bullet    
    def update(self, dt: float) -> None:
        self.position += (self.velocity * dt)
        
    def hit(self) -> bool:
        self.kill()
        return True # Has to return True because of the asteroid.split()/bounce() logic