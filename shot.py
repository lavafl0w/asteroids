from circleshape import CircleShape
from constants import SHOT_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT
import pygame

class Shot(CircleShape):
    def __init__(self, x: float, y:float) -> None:
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, 0)

    def update(self, dt: float) -> None:
        self.position += (self.velocity * dt)
        
        if (    # Remove shot if it's far outside screen boundaries
            self.position.x < -self.screen_boundary_margin
            or self.position.y < -self.screen_boundary_margin
            or self.position.x > SCREEN_WIDTH + self.screen_boundary_margin
            or self.position.y > SCREEN_HEIGHT + self.screen_boundary_margin
        ):  
            self.kill() 
        
    def hit(self) -> bool:
        self.kill()
        return True # Has to return True because of the asteroid.split()/bounce() logic