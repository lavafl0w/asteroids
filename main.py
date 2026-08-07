# INTERNAL COMPONENT IMPORTS
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
import core.setup as setup
from core.audio_manager import audio
# SYSTEM IMPORTS
import pygame
import scene_manager

def main() -> None:
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Start pygame internals and get back the screen and the clock to use
    screen, pygame_clock = setup.setup_pygame()

    # `scene_store` is a closure returned by create_scene_store().
    # It remembers the active scene objects and creates/reuses them when asked.
    scene_store = scene_manager.create_scene_store()
    
    # Delta time - track change in time between loops
    dt = 0.0

    current_scene_name = "main_menu"
    
    # 'active_scenes_dict' is what holds the returned dict from scene_store
    # this is needed due to scene_store being a function
    active_scenes_dict = scene_store(current_scene_name)
    
    next_requested_scene_name = None
    #audio.start_music(current_scene_name)
    
    #* GAME LOOP #
    while True:
        
        # Get the actual scene object for the current scene name.
        # Example: "main_menu" -> MainMenu instance.
        current_scene = active_scenes_dict[current_scene_name]
        
        events = pygame.event.get()
        
        # This makes the close button on the window work
        for event in events: 
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        #* HANDLE_EVENTS FUNCTION
        next_requested_scene_name = current_scene.handle_events(events)
        if next_requested_scene_name is not None:
            if next_requested_scene_name == 'quit':
                pygame.quit()
                return
            
            if next_requested_scene_name == "pause_menu":
                active_scenes_dict = scene_store(next_requested_scene_name, screen)
            else:
                # Get a new dict with the next scene added
                active_scenes_dict = scene_store(next_requested_scene_name)
            
            if next_requested_scene_name == "game_loop_restart":
                next_requested_scene_name = "game_loop"
                    
            # Make it the new current scene and remove change request
            current_scene_name = next_requested_scene_name
            next_requested_scene_name = None
                    
            # Switch the current scene object to what was just requested
            current_scene = active_scenes_dict[current_scene_name]   

        #* UPDATE FUNCTION
        next_requested_scene_name = current_scene.update(dt)
        if next_requested_scene_name is not None:    
            if next_requested_scene_name == 'quit':
                pygame.quit()
                return

            if next_requested_scene_name == "death_transition":
                if not isinstance(current_scene, scene_manager.GameLoop):
                    raise TypeError("death_transition can only be requested from GameLoop")

                # Get the new dict with the DeathTransition added, passing in death channel
                death_channel = current_scene.death_audio_channel
                active_scenes_dict = scene_store(next_requested_scene_name, screen, death_channel)
                
            else: 
                # It wasn't death_transition, get normal scene
                active_scenes_dict = scene_store(next_requested_scene_name) 

            # Change current scene name and remove change request
            current_scene_name = next_requested_scene_name
            next_requested_scene_name = None

            # Switch current scene to the new scene
            current_scene = active_scenes_dict[current_scene_name]
            
        #* DRAW FUNCTION
        current_scene.draw(screen)

        # After all events/checks are done
        pygame.display.flip() # Refresh display
        dt = pygame_clock.tick(60) / 1000 # Ticks at 60 FPS (divide 1000 for milliseconds)
    
    
if __name__ == "__main__":
    main()
 
