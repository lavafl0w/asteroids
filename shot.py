import pygame
import circleshape
import constants

class Shot(circleshape.CircleShape):
    def __init__(self, x: float, y:float) -> None:
        super().__init__(x, y, constants.SHOT_RADIUS)
        
    # Draw circular bullets
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, constants.LINE_WIDTH)
    
    # On update: move the bullet    
    def update(self, dt: float) -> None:
        self.position += (self.velocity * dt)