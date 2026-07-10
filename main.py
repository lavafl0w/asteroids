import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state
import player


def main() -> None:

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Create Pygame Instance
    pygame.init()

    # Internal Components
    py_clock = pygame.time.Clock() # FPS clock
    dt = 0.0 # Delta time - Change in time
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Set screen size from constants.py
    
    # Group Creation
    updatable = pygame.sprite.Group() # Empty group of updatable objects
    drawable = pygame.sprite.Group() # Empty group of drawbale objects
    
    # Populating Groups
    player.Player.containers = (updatable, drawable) # Player class -> updatable and drawable groups

    # Object Creation
    player1 = player.Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) # Create player object


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

        pygame.display.flip() # Refresh display
        dt = py_clock.tick(60) / 1000 # Ticks at 60 FPS (devision of 1000 is for milliseconds)

if __name__ == "__main__":
    main()
