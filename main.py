# INTERNAL COMPONENT IMPORTS
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
import setup
# SYSTEM IMPORTS
import pygame
import scenemanager

def main() -> None:
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Start pygame internals and get back the screen and the clock to use
    screen, pygame_clock = setup.setup_pygame()
    
    # Get audio set up, play music and assign effects
    setup.setup_sound_effects()

    # `scene_store` is a closure returned by create_scene_store().
    # It remembers the active scene objects and creates/reuses them when asked.
    scene_store = scenemanager.create_scene_store()
    
    # Delta time - track change in time between loops
    dt = 0.0

    current_scene_name = "main_menu"
    
    # 'active_scenes_dict' is what holds the returned dict from scene_store
    # this is needed due to scene_store being a function
    active_scenes_dict = scene_store(current_scene_name)
    next_requested_scene_name = None
    
    setup.start_music("main_menu")
    
    #* Game Loop #
    while True:    
        # Get the actual scene object for the current scene name.
        # Example: "main_menu" -> MainMenu instance.
        current_scene = active_scenes_dict[current_scene_name]
        
        events = pygame.event.get()
        for event in events: # This makes the close button on the window work
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        # Scenes can request a scene change from input events.
        next_requested_scene_name = current_scene.handle_events(events)
        if next_requested_scene_name is not None: # If a new scene has been requested
            # Check it's not a change to quit instead
            if next_requested_scene_name == 'quit':
                pygame.quit()
                return
            
            # Get a new dict with the next scene added
            active_scenes_dict = scene_store(next_requested_scene_name)
            
            # Make it the new current scene and remove change request
            current_scene_name = next_requested_scene_name
            next_requested_scene_name = None
            
            # Switch the current scene object to what was just requested
            current_scene = active_scenes_dict[current_scene_name]
            
        # Scenes can also request a scene change from game logic.
        # Example: GameLoop.update() can request "death_pause".
        next_requested_scene_name = current_scene.update(dt)
        if next_requested_scene_name is not None: # If a new scene was requested
            # Check if it was to quit instead
            if next_requested_scene_name == 'quit':
                pygame.quit()
                return
            
            # If the next scene is going to be 'death_pause'
            if next_requested_scene_name == "death_pause":
                # Check it didn't come from anywhere except GameLoop (to quiet the linter)
                if not isinstance(current_scene, scenemanager.GameLoop):
                    raise TypeError("death_pause can only be requested from GameLoop")
                
                # Get the death channel that was stored for death audio
                death_channel = current_scene.death_audio_channel
                # Get the new dict with the DeathPause added, passing in death channel
                active_scenes_dict = scene_store(next_requested_scene_name, death_channel)
            else: 
                # It wasn't 'death_pause', so just get the updated dict with the new Scene
                active_scenes_dict = scene_store(next_requested_scene_name)
            
            # Make it the new current scene and remove change request
            current_scene_name = next_requested_scene_name
            next_requested_scene_name = None
            
            # Switch the current scene object to the new one that was requested
            current_scene = active_scenes_dict[current_scene_name]
            
        # Draw whatever the current scene is
        current_scene.draw(screen)

        # After all events/checks are done
        pygame.display.flip() # Refresh display
        dt = pygame_clock.tick(60) / 1000 # Ticks at 60 FPS (divide 1000 for milliseconds)

if __name__ == "__main__":
    main()
 
