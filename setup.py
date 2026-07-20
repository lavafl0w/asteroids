import pygame
import player, powerups, asteroid, asteroidfield, shot
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

# Start Pygame instance, enables fonts and music
def setup_pygame() -> tuple[pygame.Surface, pygame.time.Clock, pygame.font.Font]:

    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
        
    # Set up which font to use
    font = pygame.font.SysFont(None, 20)
    
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
    music.load('assets/music_glorious_morning.mp3')
    music.set_volume(0.4)
    toggle_music()
    
    sound_effect = pygame.mixer.Sound
    
    # Player sound effects
    player.Player.death_audio = sound_effect("assets/emotional_damage.mp3")
    player.Player.shot_audio = sound_effect("assets/pew_pew.mp3")
    player.Player.player_hit_audio = sound_effect("assets/player_hit_oof.mp3")
    # Shield related sound effects
    player.ShieldPowerup.shield_activate_effect = sound_effect("assets/shield_attacktivate.mp3")
    player.ShieldPowerup.shield_deactivate_effect = sound_effect("assets/shield_pc-power-down.mp3")
    player.ShieldPowerup.shield_break_effect = sound_effect("assets/shield_minecraft-glass-break.mp3")
    player.ShieldPowerup.shield_hit_effect = sound_effect("assets/shield_tf2-critical-hit.mp3")
    # Bomb related sound effects
    powerups.Bomb.explosion_sound = sound_effect("assets/explosion.mp3")
    powerups.Bomb.countdown_sound = sound_effect("assets/bomb_countdown_beep.mp3")
    # Asteroid related sound effects
    asteroid.Asteroid.asteroid_split_sound = sound_effect("assets/orb.mp3")
    
# Creates group instances, sends them to be assigned before then returning them
def setup_groups() -> dict[str, pygame.sprite.Group]:
    groups = {}
    
    groups["updatable"] = pygame.sprite.Group()
    groups["drawable"] = pygame.sprite.Group()
    groups["asteroids"] = pygame.sprite.Group()
    groups["asteroid_interactors"] = pygame.sprite.Group()
    groups["powerup_items"] = pygame.sprite.Group()
    groups["explosion_radii"] = pygame.sprite.Group()
        
    assign_containers(groups)
    return groups

# Assigns all the sprites into groups/containers to then be more easily used
def assign_containers(g) -> None:
    
    asteroidfield.AsteroidField.containers = (g["updatable"])
    player.Player.containers = (g["updatable"], g["drawable"])
    shot.Shot.containers = (g["updatable"], g["drawable"], g["asteroid_interactors"])
    asteroid.Asteroid.containers = (g["updatable"], g["drawable"], g["asteroids"])
    powerups.Bomb.containers = (g["updatable"], g["drawable"], g["powerup_items"])
    powerups.BombExplosion.containers = (g["updatable"], g["drawable"], g["explosion_radii"])
    powerups.ShieldPowerupItem.containers = (g["updatable"], g["drawable"], g["powerup_items"])
    player.ShieldPowerup.containers = (g["updatable"], g["drawable"], g["asteroid_interactors"])
    
# Music on/off
def toggle_music() -> None:
    
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()        
        return
    
    pygame.mixer.music.play(-1)