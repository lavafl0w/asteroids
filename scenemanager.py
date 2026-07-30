from typing import Callable, List, Literal, NoReturn
import pygame
from pygame.event import Event
import setup
from player import Player
from asteroidfield import AsteroidField
from hud import HUD
from collisions import collides
from scorekeeper import ScoreKeeper
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


#FUTURE: Main menu music, button hover and click sound effect
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
                
    def handle_events(self, events) -> None | Literal['game_loop'] | Literal['quit']:
        keys = pygame.key.get_pressed()
        button_return = None
        
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
    
    def update(self, dt:float) -> None:
        #? Idk if update() is needed here
        pass
    
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
        for i in range(0, len(asteroids_group)):
            asteroid_1 = asteroids_group[i]
            for j in range(i+1, len(asteroids_group)):
                asteroid_2 = asteroids_group[j]
                if collides(asteroid_1, asteroid_2):
                    asteroid_1.bounce(asteroid_2)                

        #* Checks any other asteroid collisions
        for asteroid in self.container_groups["asteroids"]:                 
            # Player | asteroid collision
            if collides(self.player1, asteroid):
                death_result = self.player1.asteroid_hit()
                if death_result == "death":
                    #? toggle music should probably be handled by death_pause?
                    #//setup.toggle_music() # Switch music off
                    return "death_pause"

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


#TODO: This is just temporary death pause implementation, flesh it out
class DeathPause:
    def __init__(self) -> None:
        pass
    
    def handle_events(self, events: List[Event]) -> None:
        pass
    
    def draw(self, screen:pygame.Surface) -> None:
        screen.fill("red")
    
    def update(self, dt:float) -> Literal['quit']:
        # Switch music and wait until death effect is done
        setup.toggle_music()
        while pygame.mixer.get_busy(): #HACK
            continue
        
        return "quit"


class Button:
    def __init__(self, width:int, height: int, centre:tuple, font_obj:pygame.font.Font,
                 button_text:str, base_color:str, hover_color:str, press_audio: pygame.mixer.Sound | None,
                 hover_audio: pygame.mixer.Sound | None, audio_channel: pygame.mixer.Channel, callback: Callable) -> None:
        self.button = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.centre = centre
        self.font = font_obj
        self.button_text = button_text
        self.base_color = base_color
        self.hover_color = hover_color
        self.press_audio = press_audio
        self.hover_audio = hover_audio
        self.audio_channel = audio_channel
        self.callback = callback
        self.hovered_over = False
        
    def handle_events(self, event: Event) -> None:
        old_hover_state = self.hovered_over
        
        if event.type == pygame.MOUSEMOTION:
            self.hovered_over = self.button.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered_over:
            if self.press_audio:
                self.audio_channel.play(self.press_audio) # Play press audio
                
                # Wait until done
                while self.audio_channel.get_busy(): #HACK
                    continue
                
            return self.callback()
        
        # If button was just hovered over, play hover audio once
        if self.hover_audio and (not old_hover_state and self.hovered_over):
            self.audio_channel.play(self.hover_audio)
    
    def draw(self, screen:pygame.Surface) -> None:
        # Draw the overall/entire button rect -centred and coloured- on screen
        self.button.center = self.centre
        colour = self.hover_color if self.hovered_over else self.base_color
        pygame.draw.rect(screen, colour, self.button)
        
        # Make the text surface, get the rect for it and position it in centre of button
        text_surface = self.font.render(self.button_text, 1, "white")
        text_rect = text_surface.get_rect()
        text_rect.center = self.button.center
        
        # Blit the text surface on the text rect
        screen.blit(text_surface, text_rect)

        
    
Scenes = dict[str, MainMenu | GameLoop | DeathPause]
def create_scenes() -> Scenes:
    return {
        "main_menu": MainMenu(),
        "game_loop": GameLoop(),
        "death_pause": DeathPause(),
    }