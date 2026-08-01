import pygame
import setup
from typing import Literal
from player import Player
from asteroid_field import AsteroidField
from hud import HUD
from collisions import collides
from score_keeper import ScoreKeeper
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

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
