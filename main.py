# INTERNAL COMPONENT IMPORTS
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event
from debug import draw_debug
from collisions import collides
# CLASS IMPORTS
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from powerups import * #!
# SYSTEM IMPORTS
import pygame
import sys

def main() -> None:

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Start Pygame instance, enables fonts and music
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
        
    # Set up font for display
    font = pygame.font.SysFont(None, 36)
    
    # Load music track and play infinitely (-1)
    # FUTURE: call an overall sound effect assignment for music, sound effects and group assignment (?)
    music = pygame.mixer.music
    music.load('assets/music_g_m.mp3')
    music.play(-1)
    
    # Sound effects
    # FUTURE: //
    sound_effect = pygame.mixer.Sound
    death_snd_effect = sound_effect("assets/emotional_damage.mp3")
    Bomb.explosion_sound = sound_effect("assets/explosion.mp3")
    Bomb.explosion_sound.set_volume(0.20) 

    # Internal Components
    py_clock = pygame.time.Clock() # FPS clock
    dt = 0.0 # Delta time - Change in time
    screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Set screen size from constants.py
    
    # Group Creation
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    bomb_explosion = pygame.sprite.Group()
    
    # Group Assignment
    # FUTURE: //
    Player.containers = (updatable, drawable) # Player class -> updatable and drawable groups
    Asteroid.containers = (updatable, drawable, asteroids) # Astroid class -> updatable, drawable and asteroids
    AsteroidField.containers = (updatable) # AstroidField class -> updatable
    Shot.containers = (updatable, drawable, shots) # Shot class -> updatable, drawable, shots
    #Font.containers = (updatable, drawable) #? Can the font class be added to drawable container? Then it can be used to update and draw...
    Bomb.containers = (updatable, drawable, powerups) # Bomb class -> updatable, drawable, powerups
    BombExplosion.containers = (updatable, drawable, bomb_explosion)
    
    # Object Creation
    player1 = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) # Create player object
    field = AsteroidField() # Creates asteroid field
    #//debug_asteroid = Asteroid(700, 350, 40)
    #//debug_asteroid.velocity = pygame.Vector2(0,0)
    # NOTE: Future powerup hook: lightweight HUD resources or pickup systems could be introduced around this setup stage.

    #//DEBUG = True

    # Game Loop
    while True:

        # Initialise Logger
        log_state()

        # Debugging
        #// debug_data = {} if DEBUG == True else None

        # This makes the close button on the window work
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Background set
        screen.fill("black")
                
        # Creates a font screen of text to be rendered
        font_screen = font.render("Hello (not) world!", True, (255,255,255))
        screen.blit(font_screen, (10,10)) # Apply that to the main screen
        
        # NOTE: If using screen.blits(font_screen), font screen should be a list of tuples (screen, position)
        #font_screen = [(font.render("Hello (not) world!", True, (255,255,255)), (10,10)), (font.render("#################", True, (255,255,255)), (20,20))]
        #screen.blits(font_screen)
        
        # Update all things updatable with the time since last frame (dt)
        updatable.update(dt)

        # GAME EVENTS #
        for asteroid in asteroids:
            # Checks for player/asteroid collision
            #! Remember and remove this block comment lol
            '''
            if collides(player1, asteroid):
                log_event("player_hit")
                print("Game over!")
                
                # Stop music and play death sound
                music.stop()
                death_snd_effect.play()
                
                # Wait for death sound to finish then exit
                pygame.time.wait(int(death_snd_effect.get_length()*1000))
                sys.exit()
            '''                
            # Checks for any bullet/asteroid collision
            for bullet in shots:
                if collides(asteroid, bullet):
                    log_event("asteroid_shot")
                    bullet.kill() # Remove bullet object                    
                    asteroid.split() # Call asteroid split logic
            
            # Checks for any bomb_explosion/asteroid collision
            for explosion in bomb_explosion:
                if collides(asteroid, explosion):
                    asteroid.kill()
                    # FUTURE: To add further into keeping score mechanic, this could be different score because it was a bomb
                    # FUTURE: and at the end have something like "Bombs used:" "Asteroids destroyed by bombs:"
        
        # Checks for any item/powerup collision with player i.e player has picked something up
        for item in powerups:
            if collides(player1, item):
                item.activate()
        
        # Draw everything on screen that can be drawn
        for item in drawable:
            item.draw(screen)
        # FUTURE: Could add the font screen into the drawable group, and if item is a list, use screen.blits
        
        # NOTE: Draw debug data       
        #//draw_debug(screen, debug_data)

        # After all events/checks are done
        pygame.display.flip() # Refresh display
        dt = py_clock.tick(60) / 1000 # Ticks at 60 FPS (division of 1000 is for milliseconds)

if __name__ == "__main__":
    main()
