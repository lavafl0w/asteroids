# INTERNAL COMPONENT IMPORTS
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from collisions import collides
from hud import HUD
import setup
# CLASS IMPORTS
from player import Player
#//from asteroid import Asteroid
from asteroidfield import AsteroidField
#//from shot import Shot
#//from powerups import Bomb, BombExplosion
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
    container_groups = setup.setup_groups()
    
    # Delta time - track change in time between loops
    dt = 0.0
    
    # HUD display
    hud = HUD()
    
    # Object Creation
    player1 = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) # Create player object
    field = AsteroidField() # Creates asteroid field

    game_state = "playing"
    death_channel: None | pygame.mixer.Channel = None
    
    # Game Loop
    while True:
        
        # This makes the close button on the window work
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Background set
        screen.fill("black")
        
        #* Normal gameplay
        if game_state == "playing":
            # Increase game time
            ScoreKeeper.tick_time(dt)
        
            # Update all things updatable with the time since last frame (dt)
            container_groups["updatable"].update(dt)

            #* GAME EVENTS #
            # Checks any asteroid collision
            for asteroid in container_groups["asteroids"]: 
                
                # Checks player/asteroid collision
                if collides(player1, asteroid):
                    death_channel = player1.asteroid_hit()
                    if death_channel is not None: # If asteroid_hit() played sound, death_channel is no longer None
                        setup.toggle_music() # Switch music off
                        game_state = "death_pause"
                        break

                # Checks for any bullet/asteroid collision
                for bullet in container_groups["shots"]:
                    if collides(asteroid, bullet):
                        bullet.kill() # Remove bullet object                    
                        asteroid.split() # Call asteroid split logic

                # Checks for any bomb_explosion/asteroid collision
                for explosion in container_groups["explosion_radii"]:
                    if collides(asteroid, explosion):
                        ScoreKeeper.asteroid_was_exploded()
                        asteroid.kill()
                        # FUTURE: To add further into keeping score mechanic, this could be different score because it was a bomb
                        # FUTURE: and at the end have something like "Bombs used:" "Asteroids destroyed by bombs:"
        
            # Checks for any item/powerup collision with player
            for item in container_groups["powerup_items"]:
                if collides(player1, item):
                    item.activate(player1)
        
        #* If player has died            
        elif game_state == "death_pause":
            if death_channel is not None:
                # If the channel is no longer playing something
                if not death_channel.get_busy():
                    sys.exit()
                
        # Draw everything on screen that can be drawn
        for item in container_groups["drawable"]:
            item.draw(screen)
        
        # Apply the hud surface to the display over all the drawn sprites
        screen.blit(hud.hud_surface, (10,10))

        # After all events/checks are done
        pygame.display.flip() # Refresh display
        dt = pygame_clock.tick(60) / 1000 # Ticks at 60 FPS (division of 1000 is for milliseconds)

if __name__ == "__main__":
    main()
