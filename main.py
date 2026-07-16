# INTERNAL COMPONENT IMPORTS
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
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

    # Start pygame internals and get back the screen, the clock and the font to use
    screen, pygame_clock, font = setup.setup_pygame()
    
    # Get audio set up, play music and assign effects
    setup.setup_audio()
    
    # Get the groups and sprites all ready to go
    container_group = setup.setup_groups()
    
    # Delta time - track change in time between loops
    dt = 0.0
    
    # HUD display
    hud = HUD()
    
    # Object Creation
    player1 = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) # Create player object
    field = AsteroidField() # Creates asteroid field
    
    #//if debug_flags.check('ONLY_DRAW_SINGLE_ASTEROID'):
    #//    field.kill()
    #//    debug_asteroid = Asteroid(700, 350, 40)
    #//    debug_asteroid.velocity = pygame.Vector2(0,0)
        
    #//DEBUG = True

    # Game Loop
    while True:

        # Debugging
        #//debug_data = {}

        # This makes the close button on the window work
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Background set
        screen.fill("black")
                
        # Apply the hud surface to the display
        screen.blit(hud.hud_surface, (10,10))
        
        # Track game time
        ScoreKeeper.tick_time(dt)
        
        # Update all things updatable with the time since last frame (dt)
        container_group["updatable"].update(dt)

        # GAME EVENTS #
        for asteroid in container_group["asteroids"]:
            # Checks for player/asteroid collision
            if collides(player1, asteroid) and not debug_flags.check('DISABLE_PLAYER_ASTEROID_HIT'):
                print("Game over!")
                
                # Stop music and play death sound
                setup.toggle_music()
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
        
        # NOTE: Draw debug data       
        #//debug.draw_debug(screen, debug_data)

        # After all events/checks are done
        pygame.display.flip() # Refresh display
        dt = pygame_clock.tick(60) / 1000 # Ticks at 60 FPS (division of 1000 is for milliseconds)

if __name__ == "__main__":
    main()
