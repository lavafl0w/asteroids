import circleshape
import constants
import pygame

class Player(circleshape.CircleShape):
    def __init__(self, x: float, y:float) -> None:
        super().__init__(x, y, constants.PLAYER_RADIUS)
        self.rotation = 0


    # Simply create triange points
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    # Draw a triangle on the screen, coloured white with a line width from constants
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, "white", self.triangle(), constants.LINE_WIDTH)

    # Move back and forward
    def move(self, dt: float) -> None:
        unit_vector = pygame.math.Vector2(0,1) # Creates a unit vector of length 1
        rotated_vector = unit_vector.rotate(self.rotation) # Rotates vector in same direction of player
        speed_vector = rotated_vector * constants.PLAYER_SPEED * dt # Extends the length of the vector by how much the player should move in frame
        self.position += speed_vector # Makes this the new position


    # Rotates player sprite
    def rotate(self, dt: float) -> None:
        self.rotation += constants.PLAYER_TURN_SPEED * dt
    
    # On update, checks if keys have been pressed
    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]: # Move forward - Key: W
            self.move(dt)
        if keys[pygame.K_a]: # Rotates left - Key: A
            self.rotate(-dt)
        if keys[pygame.K_s]: # Move backward - Key : S
            self.move(-dt)
        if keys[pygame.K_d]: # Rotates right - Key: D
            self.rotate(dt)