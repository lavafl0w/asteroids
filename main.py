# INTERNAL COMPONENT IMPORTS
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from collisions import collides
from hud import HUD
import setup
# CLASS IMPORTS
from player import Player
from asteroidfield import AsteroidField
from scorekeeper import ScoreKeeper
# SYSTEM IMPORTS
import pygame
import sys
import scenemanager

def main() -> None:

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Start pygame internals and get back the screen, the clock and the font to use
    screen, pygame_clock, font = setup.setup_pygame()
    
    # Get audio set up, play music and assign effects
    setup.setup_audio()
    
    scenes = scenemanager.create_scenes(font)
    
    # Delta time - track change in time between loops
    dt = 0.0

    game_state = "main_menu"
    death_channel: None | pygame.mixer.Channel = None
    
    #* Game Loop #
    while True:
        
        events = pygame.event.get()
        # This makes the close button on the window work
        for event in events:
            if event.type == pygame.QUIT:
                return
        
        # NOTE: See scenemanager for explanation rn
              
        game_state = scenes[game_state].handle_events(events)

        scenes[game_state].draw(screen)
        scenes[game_state].update(dt)

        # After all events/checks are done
        pygame.display.flip() # Refresh display
        dt = pygame_clock.tick(60) / 1000 # Ticks at 60 FPS (division of 1000 is for milliseconds)

if __name__ == "__main__":
    main()
 