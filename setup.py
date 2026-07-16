import pygame
import player, powerups, asteroid, asteroidfield, shot
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

# Start Pygame instance, enables fonts and music
def setup_pygame() -> tuple[pygame.Surface, pygame.time.Clock, pygame.font.Font]:

    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
        
    # Set up which font to use
    font = pygame.font.SysFont(None, 36)
    
    # Creates an internal clock
    pygame_clock = pygame.time.Clock()
    
    # Sets the screen to the dimensions
    screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Returns these for use in main.py
    return screen, pygame_clock, font
    
# Handles audio setup like music and assigning sound effects
def setup_audio() -> None:
    
    # Load music and play
    music = pygame.mixer.music
    music.load('assets/music_g_m.mp3')
    toggle_music()
    
    sound_effect = pygame.mixer.Sound
    
    # Player sound effects
    player.Player.death_audio = sound_effect("assets/emotional_damage.mp3")
    player.Player.shot_audio = sound_effect("assets/pew-pew-lame-sound-effect.mp3")
    # Bomb related sound effects
    powerups.Bomb.explosion_sound = sound_effect("assets/explosion.mp3")
    powerups.Bomb.tick_sound = sound_effect("assets/bomb_tick.mp3")
    # Asteroid related sound effects
    asteroid.Asteroid.asteroid_split_sound = sound_effect("assets/orb.mp3")
    
# Creates group instances, sends them to be assigned before then returning them
def setup_groups() -> dict[str, pygame.sprite.Group]:
    groups = {}
    
    groups["updatable"] = pygame.sprite.Group()
    groups["drawable"] = pygame.sprite.Group()
    groups["asteroids"] = pygame.sprite.Group()
    groups["shots"] = pygame.sprite.Group()
    groups["powerup_items"] = pygame.sprite.Group()
    groups["explosion_radii"] = pygame.sprite.Group()
        
    assign_containers(groups)
    return groups

# Assigns all the sprites into groups/containers to then be more easily used
def assign_containers(g) -> None:
    
    asteroidfield.AsteroidField.containers = (g["updatable"]) # AstroidField class -> updatable
    player.Player.containers = (g["updatable"], g["drawable"]) # Player class -> updatable and drawable groups
    shot.Shot.containers = (g["updatable"], g["drawable"], g["shots"]) # Shot class -> updatable, drawable, shots
    asteroid.Asteroid.containers = (g["updatable"], g["drawable"], g["asteroids"]) # Astroid class -> updatable, drawable and asteroids
    powerups.Bomb.containers = (g["updatable"], g["drawable"], g["powerup_items"]) # Bomb class -> updatable, drawable, powerups
    powerups.BombExplosion.containers = (g["updatable"], g["drawable"], g["explosion_radii"])

# Music on/off
def toggle_music() -> None:
    
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()        
        return
    
    pygame.mixer.music.play(-1)