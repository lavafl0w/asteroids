from typing import Callable, Generic, List, Literal, TypeVar
import pygame
from pygame.event import Event
import setup
from player import Player
from asteroidfield import AsteroidField
from hud import HUD
from collisions import collides
from scorekeeper import ScoreKeeper
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

MainMenuAction = Literal['game_loop', 'quit']
T = TypeVar("T")

class MainMenu:
    start_hover_audio: pygame.mixer.Sound | None = None
    quit_hover_audio: pygame.mixer.Sound | None = None
    start_press_audio: pygame.mixer.Sound | None = None
    quit_press_audio: pygame.mixer.Sound | None = None
    
    def __init__(self) -> None:
        self.title_font = pygame.font.Font(None, 64)
        self.button_font = pygame.font.Font(None, 32)
        self.menu_background = pygame.image.load("assets/amazing_menu_background.png")
        self.audio_channel = pygame.mixer.find_channel(True) # Force a channel in case none are available
        
        self.start_button = Button(150, 75, (SCREEN_WIDTH/2, 350), self.button_font, 
                                    "Start Game", "red", "green", self.start_press_audio, self.start_hover_audio,
                                    self.audio_channel, self.start_game)
        self.quit_button = Button(150, 75, (SCREEN_WIDTH/2, 650), self.button_font, 
                                    "Quit", "red", "green", self.quit_press_audio, self.quit_hover_audio, 
                                    self.audio_channel, self.quit_game)
                
    def handle_events(self, events) -> None | MainMenuAction:
        button_return = None
        if self.start_button.pending_callback or self.quit_button.pending_callback:
            return
        
        for event in events:
            button_return = self.start_button.handle_events(event)
            if button_return:
                return button_return

            button_return = self.quit_button.handle_events(event)
            if button_return:
                return button_return
            
    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.menu_background, (0,0))
        
        title_surface = self.title_font.render("ASTEROIDS", 1, "white")
        title_rect = title_surface.get_rect()
        title_rect.center = (int(SCREEN_WIDTH/2), 100)
        
        screen.blit(title_surface, title_rect)
        
        self.start_button.draw(screen)
        self.quit_button.draw(screen)
    
    def update(self, dt:float) -> None | MainMenuAction:      
        button_return = self.start_button.update()
        if button_return:
            return button_return
        
        button_return = self.quit_button.update()
        if button_return:
            return button_return
        
    
    def start_game(self) -> Literal['game_loop']:
        setup.start_music("game_loop") # Start music for game loop
        return "game_loop"
    
    def quit_game(self) -> Literal['quit']:
        return "quit"


class GameLoop:
    def __init__(self) -> None:
        # Load background image
        self.background = pygame.image.load("assets/space_background.png")
    
        # Get the groups and sprites all ready to go
        self.container_groups = setup.setup_assign_groups()
        
        # Object Creation
        self.player1 = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.asteroid_field = AsteroidField()
        
        # HUD display
        self.hud = HUD()
        
        self.death_audio_channel: pygame.mixer.Channel | None = None
    
    #FUTURE: Escape should be pause menu    
    def handle_events(self, events) -> None | Literal['main_menu']:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "main_menu"
    
    def draw(self, screen: pygame.Surface) -> None:
        # Wipe with background image 
        screen.blit(self.background, (0,0))

        for item in self.container_groups["drawable"]:
            item.draw(screen)
        
        # Apply the hud surface to the display over drawn sprites
        screen.blit(self.hud.hud_surface, (10,10))
    
    def update(self, dt:float) -> None | Literal['death_pause']:
        # Increase game time
        ScoreKeeper.tick_time(dt)
        
        # Update all things updatable with the time since last frame (dt)
        self.container_groups["updatable"].update(dt)
        
        # Update HUD values
        self.hud.update_hud(dt)
        
        #* GAME EVENTS #
        #* Checks item/powerup | player collision
        for item in self.container_groups["powerup_items"]:
            if collides(self.player1, item):
                item.activate(self.player1)
        
        #* Checks asteroid | asteroid collision (for bouncing)
        asteroids_group = list(self.container_groups["asteroids"])
        for i in range(0, len(asteroids_group)): # Iterate through all asteroids (asteroid_1)
            asteroid_1 = asteroids_group[i] 
            
            for j in range(i+1, len(asteroids_group)): # Iterate through all asteroids after asteroid_1
                asteroid_2 = asteroids_group[j]
                
                if collides(asteroid_1, asteroid_2): # Check collision
                    asteroid_1.bounce(asteroid_2)                

        #* Checks any other asteroid collisions
        for asteroid in self.container_groups["asteroids"]:                 
            # Player | asteroid collision
            if collides(self.player1, asteroid):
                death_channel = self.player1.asteroid_hit()
                if death_channel: # Channel was returned, so must have died
                    self.death_audio_channel = death_channel # Store it to be accessed later
                    return 'death_pause'

            # Bullet/shield | asteroid collision
            for interactor in self.container_groups["asteroid_interactors"]:
                if collides(asteroid, interactor):
                    if interactor.hit(): # If the hit connected...            
                        asteroid.split() # Call asteroid split logic
                    else:
                        asteroid.bounce(interactor) # Bounce away from it (for shield on cooldown)
                    
            # Bomb_explosion | asteroid collision
            for explosion in self.container_groups["explosion_radii"]:
                if collides(asteroid, explosion):
                    ScoreKeeper.asteroid_was_exploded()
                    asteroid.kill()
                    #FUTURE: To add further into keeping score mechanic, 
                    #FUTURE: this could be different score because it was a bomb


class DeathPause:
    def __init__(self, death_audio_channel: pygame.mixer.Channel) -> None:
        self.death_audio_channel = death_audio_channel
    
    def handle_events(self, events: List[Event]) -> None:
        pass
    
    def draw(self, screen:pygame.Surface) -> None:
        #TODO: Temporary death pause screen visual, need to design
        screen.fill("red")
    
    def update(self, dt:float) -> None | Literal['quit']:
        # Switch music and wait until death effect is done
        if pygame.mixer.music.get_busy():
            setup.toggle_music()
        
        if not self.death_audio_channel.get_busy():        
            return "quit"
        

class Button(Generic[T]):
    def __init__(self, width:int, height: int, centre:tuple, font_obj:pygame.font.Font,
                 button_text:str, base_color:str, hover_color:str, press_audio: pygame.mixer.Sound | None,
                 hover_audio: pygame.mixer.Sound | None, audio_channel: pygame.mixer.Channel,
                 callback: Callable[[], T]) -> None:
        self.button = pygame.Rect(0, 0, width, height)
        self.button.center = centre
        self.font = font_obj
        self.button_text = button_text
        self.base_color = base_color
        self.hover_color = hover_color
        self.press_audio = press_audio
        self.hover_audio = hover_audio
        self.audio_channel = audio_channel
        self.callback = callback
        self.hovered_over = False
        self.pending_callback = False
        
    def handle_events(self, event: Event) -> T | None:
        old_hover_state = self.hovered_over
        
        if event.type == pygame.MOUSEMOTION:
            self.hovered_over = self.button.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered_over:
            if self.press_audio:
                self.audio_channel.play(self.press_audio) # Play press audio
                self.pending_callback = True
                return
            
            return self.callback() # Guard against audio not being assigned
        
        # If button isn't pending_callback was just hovered over, play hover audio once
        if self.hover_audio and not self.pending_callback and (not old_hover_state and self.hovered_over):
            self.audio_channel.play(self.hover_audio)
    
    def draw(self, screen:pygame.Surface) -> None:
        # Draw the overall/entire button rect coloured on screen
        colour = self.hover_color if self.hovered_over else self.base_color
        pygame.draw.rect(screen, colour, self.button)
        
        # Make the text surface, get the rect for it and position it in centre of button
        text_surface = self.font.render(self.button_text, 1, "white")
        text_rect = text_surface.get_rect()
        text_rect.center = self.button.center
        
        # Blit the text surface on the text rect
        screen.blit(text_surface, text_rect)
        
    def update(self) -> T | None:
        if not self.audio_channel.get_busy() and self.pending_callback == True:
            self.pending_callback = False
            return self.callback()


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

