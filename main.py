import pygame
import sys

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event

from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main() -> None:

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Create Pygame Instance
    pygame.init()

    # Internal Components
    py_clock = pygame.time.Clock() # FPS clock
    dt = 0.0 # Delta time - Change in time
    screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Set screen size from constants.py
    
    # Group Creation
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    # Group Assignment
    Player.containers = (updatable, drawable) # Player class -> updatable and drawable groups
    Asteroid.containers = (updatable, drawable, asteroids) # Astroid class -> updatable, drawable and asteroids
    AsteroidField.containers = (updatable) # AstroidField class -> updatable
    Shot.containers = (updatable, drawable, shots)

    # Object Creation
    player1 = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) # Create player object
    field = AsteroidField() # Creates asteroid field

    # Game Loop
    while True:

        log_state() # Start logger

        # This makes the close button on the window work
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black") # Set background
        
        for item in drawable:
            item.draw(screen) # Draw everything in drawable group
        
        updatable.update(dt) # Update any movement in updatable group
        
        for asteroid in asteroids:
            # Checks for player/asteroid collision
            if asteroid.collides_with(player1) == True:
                log_event("player_hit")
                print("Game over!")
                sys.exit()
                
            # Checks for any bullet/asteroid collision
            for bullet in shots:
                if asteroid.collides_with(bullet) == True:
                    log_event("asteroid_shot")
                    bullet.kill()
                    asteroid.split()

        pygame.display.flip() # Refresh display
        dt = py_clock.tick(60) / 1000 # Ticks at 60 FPS (division of 1000 is for milliseconds)

if __name__ == "__main__":
    main()
