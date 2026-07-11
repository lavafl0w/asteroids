# INTERNAL COMPONENT IMPORTS
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event
# CLASS IMPORTS
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
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
    music = pygame.mixer.music
    music.load('assets/music_g_m.mp3')
    music.play(-1)
    
    # Sound effects
    sound_effect = pygame.mixer.Sound
    death_snd_effect = sound_effect("assets/emotional_damage.mp3")

    # Internal Components
    py_clock = pygame.time.Clock() # FPS clock
    dt = 0.0 # Delta time - Change in time
    screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Set screen size from constants.py
    
    # Group Creation
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    # Possible extension point: collectible pickups may want their own sprite group in this setup.
    
    # Group Assignment
    Player.containers = (updatable, drawable) # Player class -> updatable and drawable groups
    Asteroid.containers = (updatable, drawable, asteroids) # Astroid class -> updatable, drawable and asteroids
    AsteroidField.containers = (updatable) # AstroidField class -> updatable
    Shot.containers = (updatable, drawable, shots) # Shot class -> updatable, drawable, shots

    # Object Creation
    player1 = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) # Create player object
    field = AsteroidField() # Creates asteroid field
    # NOTE: Future powerup hook: lightweight HUD resources or pickup systems could be introduced around this setup stage.

    # Game Loop
    while True:

        log_state() # Start logger

        # This makes the close button on the window work
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black") # Set background
        
        # Creates a font screen of what text will be rendered
        font_screen = font.render("Hello (not) world!", True, (255,255,255))
        screen.blit(font_screen, (10,10)) # Apply that to the main screen
        
        # NOTE: Font screen should be a list of tuples (screen, position) that can then be used by screen.blits(font_screen)
        #font_screen = [(font.render("Hello (not) world!", True, (255,255,255)), (10,10)), (font.render("#################", True, (255,255,255)), (20,20))]
        #screen.blits(font_screen)
        
        for item in drawable:
            item.draw(screen) # Draw everything in drawable group
        # TODO: Could add the font screen into the drawable group, and if item is a list, use screen.blits
        
        updatable.update(dt) # Update any movement in updatable group
        
        for asteroid in asteroids:
            # NOTE: Future powerup hook: protected-hit handling and pickup collisions can slot into this collision section.
            # Checks for player/asteroid collision
            if asteroid.collides_with(player1) == True:
                log_event("player_hit")
                print("Game over!")
                
                # Stop music and play death sound
                music.stop()
                death_snd_effect.play()
                
                # Wait for death sound to finish then exit
                pygame.time.wait(int(death_snd_effect.get_length()*1000))
                sys.exit()
                
            # Checks for any bullet/asteroid collision
            for bullet in shots:
                if asteroid.collides_with(bullet) == True:
                    log_event("asteroid_shot")
                    bullet.kill() # Remove bullet object
                    asteroid.split() # Call asteroid split logic

        pygame.display.flip() # Refresh display
        dt = py_clock.tick(60) / 1000 # Ticks at 60 FPS (division of 1000 is for milliseconds)

if __name__ == "__main__":
    main()
