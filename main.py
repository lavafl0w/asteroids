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
    
    #? Have a look at maybe changing the terms from scenes to something else
    scenes = scenemanager.create_scenes(font)
    
    # Delta time - track change in time between loops
    dt = 0.0

    game_state = "main_menu"
    #//death_channel: None | pygame.mixer.Channel = None
    
    #* Game Loop #
    while True:
        next_scene = None # So both handle_events and update can request a scene change
        events = pygame.event.get()
        
        # This makes the close button on the window work
        for event in events:
            if event.type == pygame.QUIT:
                return
              
        next_scene = scenes[game_state].handle_events(events)
        if next_scene is not None:
            game_state = next_scene
            
        next_scene = scenes[game_state].update(dt)
        if next_scene is not None:
            game_state = next_scene
            
        scenes[game_state].draw(screen)

        # After all events/checks are done
        pygame.display.flip() # Refresh display
        dt = pygame_clock.tick(60) / 1000 # Ticks at 60 FPS (divide 1000 for milliseconds)

if __name__ == "__main__":
    main()
 