import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state


def main():

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init() # Create pygame instance

    py_clock = pygame.time.Clock() # Create FPS clock
    dt = 0 # Delta time - Change in time
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Set screen size as defined in constants.py

    while True:

        log_state()

        # This makes the close button on the window work
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black") # Background
        pygame.display.flip()

        dt = py_clock.tick(60) / 1000

if __name__ == "__main__":
    main()
