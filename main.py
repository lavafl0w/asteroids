# INTERNAL COMPONENT IMPORTS
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
#//from logger import log_state, log_event
from debug import *
from collisions import collides
from hud import HUD
import debug_flags
import setup
# CLASS IMPORTS
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from powerups import Bomb, BombExplosion
from scorekeeper import ScoreKeeper
# SYSTEM IMPORTS
import pygame
import sys

def main() -> None:

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen, pygame_clock, font = setup.setup_pygame()
    audio_bank = setup.setup_audio()
    container_group = setup.setup_groups()
    
    #music = audio_dict["music"]
    #sound_effect = audio_dict["sound_effect"]
    # Start Pygame instance, enables fonts and music
    #pygame.init()
    #pygame.font.init()
    #pygame.mixer.init()
        
    # Set up font for display
    #font = pygame.font.SysFont(None, 36)
    
    # Load music track and play infinitely (-1)
    #audio_bank["music"].play(-1)
    
    # Sound effects
    #death_audio = audio_bank["death_audio"]
    #Bomb.explosion_sound = audio_bank["bomb_explosion"]
    #Bomb.tick_sound = audio_bank["bomb_tick"]
    #Asteroid.asteroid_split_sound = audio_bank["asteroid_split"]

    # Internal Components
    #pygame_clock = pygame.time.Clock() # FPS clock
    dt = 0.0 # Delta time - Change in time
    #screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Set screen size from constants.py
    hud = HUD()
    
    # Group Creation
    #updatable = pygame.sprite.Group()
    #drawable = pygame.sprite.Group()
    #asteroids = pygame.sprite.Group()
    #shots = pygame.sprite.Group()
    #powerups = pygame.sprite.Group()
    #bomb_explosion = pygame.sprite.Group()
    
    # Group Assignment
    #AsteroidField.containers = (updatable) # AstroidField class -> updatable
    #Player.containers = (updatable, drawable) # Player class -> updatable and drawable groups
    #Shot.containers = (updatable, drawable, shots) # Shot class -> updatable, drawable, shots
    #Asteroid.containers = (updatable, drawable, asteroids) # Astroid class -> updatable, drawable and asteroids
    #Bomb.containers = (updatable, drawable, powerups) # Bomb class -> updatable, drawable, powerups
    #BombExplosion.containers = (updatable, drawable, bomb_explosion)
    #Font.containers = (updatable, drawable) #? Can the font class be added to drawable container? Then it can be used to update and draw...
    
    # Object Creation
    player1 = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) # Create player object
    field = AsteroidField() # Creates asteroid field
    if debug_flags.check('ONLY_DRAW_SINGLE_ASTEROID'):
        field.kill()
        debug_asteroid = Asteroid(700, 350, 40)
        debug_asteroid.velocity = pygame.Vector2(0,0)
    # NOTE: Future powerup hook: lightweight HUD resources or pickup systems could be introduced around this setup stage.

    #//DEBUG = True

    # Game Loop
    while True:

        # Initialise Logger
        #//log_state()

        # Debugging
        #//debug_data = {}

        # This makes the close button on the window work
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Background set
        screen.fill("black")
                
        # Creates a font screen of text to be rendered
        font_screen = font.render("Hello (not) world!", True, (255,255,255))
        screen.blit(hud.hud_surface, (10,10)) # Apply that to the main screen
        
        # NOTE: If using screen.blits(font_screen), font screen should be a list of tuples (screen, position)
        #font_screen = [(font.render("Hello (not) world!", True, (255,255,255)), (10,10)), (font.render("#################", True, (255,255,255)), (20,20))]
        #screen.blits(font_screen)
        
        ScoreKeeper.tick_time(dt)
        
        # Update all things updatable with the time since last frame (dt)
        container_group["updatable"].update(dt)

        # GAME EVENTS #
        for asteroid in container_group["asteroids"]:
            # Checks for player/asteroid collision
            if collides(player1, asteroid) and not debug_flags.check('DISABLE_PLAYER_ASTEROID_HIT'):
                print("Game over!")
                
                # Stop music and play death sound
                audio_bank["music"].stop()
                if player1.death_audio is not None:
                    player1.death_audio.play()
                    pygame.time.wait(int(player1.death_audio.get_length()*1000))
                # Wait for death sound to finish then exit
                sys.exit()

            # Checks for any bullet/asteroid collision
            for bullet in container_group["shots"]:
                if collides(asteroid, bullet):
                    bullet.kill() # Remove bullet object                    
                    asteroid.split() # Call asteroid split logic
            
            # Checks for any bomb_explosion/asteroid collision
            for explosion in container_group["explosion_radii"]:
                if collides(asteroid, explosion):
                    ScoreKeeper.asteroid_was_exploded()
                    asteroid.kill()
                    # FUTURE: To add further into keeping score mechanic, this could be different score because it was a bomb
                    # FUTURE: and at the end have something like "Bombs used:" "Asteroids destroyed by bombs:"
        
        # Checks for any item/powerup collision with player i.e player has picked something up
        for item in container_group["powerup_items"]:
            if collides(player1, item):
                item.activate()
        
        # Draw everything on screen that can be drawn
        for item in container_group["drawable"]:
            item.draw(screen)
        # FUTURE: Could add the font screen into the drawable group, and if item is a list, use screen.blits
        
        # NOTE: Draw debug data       
        #//debug.draw_debug(screen, debug_data)

        # After all events/checks are done
        pygame.display.flip() # Refresh display
        dt = pygame_clock.tick(60) / 1000 # Ticks at 60 FPS (division of 1000 is for milliseconds)

if __name__ == "__main__":
    main()
