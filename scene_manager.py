import pygame
from typing import Callable
from scenes.main_menu import MainMenu
from scenes.game_loop import GameLoop
from scenes.death_pause import DeathPause

Scene = MainMenu | GameLoop | DeathPause
SceneStore = dict[str, Scene]

def create_scene_store() -> Callable[..., SceneStore]:
    # This dictionary lives inside the closure, so it persists between calls to
    # prepare_scene() without needing to be global.
    active_scenes: SceneStore = {}
    
    def prepare_scene(scene_name: str, death_channel: pygame.mixer.Channel | None = None) -> SceneStore:
        """ This function is returned to main.py as `scene_store`.
        main.py asks for a scene by name, and this function makes sure the
        correct scene object exists in active_scenes before returning the dict."""
        nonlocal active_scenes
        
        # If the request was to restart the game loop fresh
        if scene_name == "game_loop_restart":
            
            # Rename to game_loop so the rest can be handled by scene creation code below
            scene_name = "game_loop" 
            
            if active_scenes.get(scene_name) is None: # Guard against possible error
                raise Exception("somehow trying to restart game loop without it existing")
            
            del active_scenes[scene_name] # Delete current game loop
        
        # If the scene already exists, skip the scene creation
        if active_scenes.get(scene_name) is not None:
            return active_scenes
        
        # Creates a scene based on what was passed into scene_name
        if scene_name == "main_menu":
            active_scenes[scene_name] = MainMenu()        
        elif scene_name == "game_loop":
            active_scenes[scene_name] = GameLoop()   
        elif scene_name == "death_pause":
            if death_channel is None:
                raise ValueError("death_pause needs the player death audio channel")
            active_scenes[scene_name] = DeathPause(death_channel)
            
        return active_scenes
    
    return prepare_scene

