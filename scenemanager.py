from typing import Callable, List, Literal

import pygame
from pygame.event import Event
import setup
from player import Player
from asteroidfield import AsteroidField
from hud import HUD
from collisions import collides
from scorekeeper import ScoreKeeper
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

'''
Right now, main is set at main_menu, which paints the screen orange
when handle events is called, if space is pressed, it returns game_loop, which draws the main game

this works in reverse also with gameloop and the esc key back to main menu
'''

class MainMenu:
    def __init__(self, font: pygame.font.Font) -> None:
        self.menu_background = "orange"
        self.test_button = Button(250, 250, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), font, 
                                  "text", "red", "green", self.start_game)
                
    def handle_events(self, events) -> None | Literal['game_loop']:
        for event in events:
            return self.test_button.handle_events(event)
        #//for event in events:
        #//    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #//        return "game_loop"
    
    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(self.menu_background)
        self.test_button.draw(screen)
    
    def update(self, dt:float) -> None:
        pass
    
    def start_game(self) -> Literal['game_loop']:
        print("start")
        return "game_loop"


class GameLoop:
    def __init__(self, font: pygame.font.Font) -> None:
        # Load background image
        self.background = pygame.image.load("assets/space_background.png")
    
        # Get the groups and sprites all ready to go
        self.container_groups = setup.setup_groups()
        
        # Object Creation
        self.player1 = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.asteroid_field = AsteroidField()
        
        # HUD display
        self.hud = HUD(font)
        
    def handle_events(self, events) -> None | Literal['main_menu']:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "main_menu"
    
    def draw(self, screen: pygame.Surface) -> None:
        # Use background image 
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
                death_channel = self.player1.asteroid_hit()
                if death_channel is not None: # If asteroid_hit() played sound, death_channel is no longer None
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
                    # FUTURE: To add further into keeping score mechanic, this could be different score because it was a bomb
                    # FUTURE: and at the end have something like "Bombs used:" "Asteroids destroyed by bombs:"


#TODO: This is just temporary death pause implementation, flesh it out
#NOTE: Old death_channel test before exit probs wont work anymore as it stands
#NOTE: cause death pause doesnt have access to death channel
class DeathPause:
    def __init__(self, font: pygame.font.Font):
        pass
    
    def handle_events(self, events: List[Event]):
        pass
    
    def draw(self, screen:pygame.Surface):
        screen.fill("red")
    
    def update(self, dt:float):
        setup.toggle_music()


class Button:
    def __init__(self, width:int, height: int, centre:tuple, font_obj:pygame.font.Font,
                 button_text:str, base_color:str, hover_color:str, callback: Callable) -> None:
        self.button = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.centre = centre
        self.font = font_obj
        self.button_text = button_text
        self.base_color = base_color
        self.hover_color = hover_color
        self.callback = callback
        self.hovered_over = False
        
    def handle_events(self, event: Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.hovered_over = self.button.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered_over:
            return self.callback()
    
    def draw(self, screen:pygame.Surface):
        button = self.button
        button.center = self.centre
        
        colour = self.hover_color if self.hovered_over else self.base_color
        pygame.draw.rect(screen, colour, button)
        #text_rect = pygame.Rect(self.button.copy())
        
        
    
    
    
Scenes = dict[str, MainMenu | GameLoop | DeathPause]
def create_scenes(font) -> Scenes:
    return {
        "main_menu": MainMenu(font),
        "game_loop": GameLoop(font),
        "death_pause": DeathPause(font),
    }


        #

        #    

#
        #    
        #
        
        #        #* NORMAL GAMEPLAY # 
        #if game_state == "playing":
        #    
        ##* If player has died #             
        #elif game_state == "death_pause":
        #    if death_channel is not None:
        #        # If the channel is no longer playing something
        #        if not death_channel.get_busy():
        #            sys.exit()
        #        

        #
