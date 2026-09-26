import pygame
from player import Player, ShieldPowerup
from asteroid_field import AsteroidField
from shot import Shot
from asteroid import Asteroid
from powerups.bomb import Bomb, BombExplosion
from powerups.pickups import ShieldPowerupItem, HealthPickup, RapidFirePickup
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from core.audio_manager import audio
import logging
import logging.handlers

logger = logging.getLogger("asteroids")

def setup_logger() -> logging.Logger:
    """Create logger with file rotation & formatting, as well as handler to log to console"""
    logger = logging.getLogger("asteroids")
    using_fallback_log_location = False
    
    try:
        handler = logging.handlers.RotatingFileHandler(
                      "logs/asteroids.log", maxBytes=2 * 1024 * 1024, backupCount=2)
    except FileNotFoundError:
        handler = logging.handlers.RotatingFileHandler(
                              "asteroids.log", maxBytes=2 * 1024 * 1024, backupCount=2)
        using_fallback_log_location = True
        
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s", datefmt="%H:%M:%S")
    handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(console_handler)

    logger.setLevel(logging.INFO)
    console_handler.setLevel(logging.INFO)
    
    if using_fallback_log_location:
        logger.warning("Log directory missing; using asteroids.log in the working directory")
    else:
        logger.info("Logging to logs/asteroids.log")
        
    return logger

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
    
    logger.debug("Groups set up successfully")
        
    assign_containers(groups)
    return groups

def assign_containers(g) -> None:
    """Assigns all the sprite containers to relevant groups to then be more easily used"""    
    AsteroidField.containers = (g["updatable"])
    Asteroid.containers = (g["updatable"], g["drawable"], g["asteroids"])
    
    Player.containers = (g["updatable"], g["drawable"])
    ShieldPowerup.containers = (g["updatable"], g["drawable"], g["asteroid_interactors"])
    Shot.containers = (g["updatable"], g["drawable"], g["asteroid_interactors"])
    
    Bomb.containers = (g["updatable"], g["drawable"], g["powerup_items"])
    BombExplosion.containers = (g["updatable"], g["drawable"], g["explosion_radii"])
    ShieldPowerupItem.containers = (g["updatable"], g["drawable"], g["powerup_items"])
    HealthPickup.containers = (g["updatable"], g["drawable"], g["powerup_items"])
    RapidFirePickup.containers = (g["updatable"], g["drawable"], g["powerup_items"])

    logger.debug("Sprite group assignments done")