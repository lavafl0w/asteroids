import pygame
import player, powerups, asteroid, asteroid_field, shot
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from core.audio_manager import audio

def setup_pygame() -> tuple[pygame.Surface, pygame.time.Clock]:
    """Start Pygame instance, creates the clock and display screen"""
    pygame.init()
    pygame.mixer.init()
    
    # Assign sound effects
    audio.setup_sound_effects()

    # Creates an internal clock
    pygame_clock = pygame.time.Clock()
    
    # Sets the screen to the dimensions and sets title
    screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ASTEROIDSS!!!11!111!!1!!!")
    
    # Returns these for use in main.py
    return screen, pygame_clock

def setup_assign_groups() -> dict[str, pygame.sprite.Group]:
    """Creates group instances, assigns relevent class containers to them then returns for use"""
    groups = {}
    
    groups["updatable"] = pygame.sprite.Group()
    groups["drawable"] = pygame.sprite.Group()
    groups["asteroids"] = pygame.sprite.Group()
    groups["asteroid_interactors"] = pygame.sprite.Group()
    groups["powerup_items"] = pygame.sprite.Group()
    groups["explosion_radii"] = pygame.sprite.Group()
        
    assign_containers(groups)
    return groups

def assign_containers(g) -> None:
    """Assigns all the sprite containers to relevant groups to then be more easily used"""    
    asteroid_field.AsteroidField.containers = (g["updatable"])
    asteroid.Asteroid.containers = (g["updatable"], g["drawable"], g["asteroids"])
    
    player.Player.containers = (g["updatable"], g["drawable"])
    player.ShieldPowerup.containers = (g["updatable"], g["drawable"], g["asteroid_interactors"])
    shot.Shot.containers = (g["updatable"], g["drawable"], g["asteroid_interactors"])
    
    powerups.Bomb.containers = (g["updatable"], g["drawable"], g["powerup_items"])
    powerups.BombExplosion.containers = (g["updatable"], g["drawable"], g["explosion_radii"])
    powerups.ShieldPowerupItem.containers = (g["updatable"], g["drawable"], g["powerup_items"])
    powerups.HealthPickup.containers = (g["updatable"], g["drawable"], g["powerup_items"])
