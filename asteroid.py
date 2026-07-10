import circleshape
import constants
import pygame


class Asteroid(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
    
    # Draw circular asteroids
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, constants.LINE_WIDTH)
    
    # On update: move the astroid    
    def update(self, dt: float) -> None:
        self.position += (self.velocity * dt)