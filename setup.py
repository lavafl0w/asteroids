import pygame
import player, powerups, asteroid, asteroidfield, shot, scenemanager
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

def setup_pygame() -> tuple[pygame.Surface, pygame.time.Clock]:
    """Start Pygame instance, creates the clock and display screen"""
    pygame.init()
    pygame.mixer.init()

    # Creates an internal clock
    pygame_clock = pygame.time.Clock()
    
    # Sets the screen to the dimensions and sets title
    screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ASTEROIDSS!!!11!111!!1!!!")
    
    # Returns these for use in main.py
    return screen, pygame_clock

def start_music(scene) -> None:
    """Load music for scene and play"""
    music = pygame.mixer.music
    
    if music.get_busy():
        toggle_music()
        music.unload()
    
    if scene == "main_menu":
        music.load('assets/music_san_andreas.mp3')
        music.set_volume(0.6)
        toggle_music()
    
    elif scene == "game_loop":
        music.load('assets/music_glorious_morning.mp3')
        music.set_volume(0.4)
        toggle_music()

def setup_sound_effects() -> None:
    """Handles assigning sound effects"""    
    sound_effect = pygame.mixer.Sound
    
    # Scenemanager sound effects
    scenemanager.MainMenu.start_hover_audio = sound_effect("assets/route_jingle.mp3")
    scenemanager.MainMenu.quit_hover_audio = sound_effect("assets/bruh.mp3")
    scenemanager.MainMenu.start_press_audio = sound_effect("assets/good_boy.mp3")
    scenemanager.MainMenu.quit_press_audio = sound_effect("assets/vine_boom.mp3")
    # Player sound effects
    player.Player.death_audio = sound_effect("assets/emotional_damage.mp3")
    player.Player.shot_audio = sound_effect("assets/pew_pew.mp3")
    player.Player.player_hit_audio = sound_effect("assets/player_hit_oof.mp3")
    player.Player.player_low_health_audio = sound_effect("assets/fable-health-low.mp3")
    # Shield related sound effects
    player.ShieldPowerup.shield_activate_effect = sound_effect("assets/shield_attacktivate.mp3")
    player.ShieldPowerup.shield_deactivate_effect = sound_effect("assets/shield_pc-power-down.mp3")
    player.ShieldPowerup.shield_break_effect = sound_effect("assets/shield_minecraft-glass-break.mp3")
    player.ShieldPowerup.shield_hit_effect = sound_effect("assets/shield_tf2-critical-hit.mp3")
    # Health related sound effects
    player.Player.player_life_maximum_audio = sound_effect("assets/maximum-patrona-lifes.mp3")
    player.Player.player_life_pickup_audio = sound_effect("assets/extra-lifee.mp3")
    # Bomb related sound effects
    powerups.Bomb.explosion_sound = sound_effect("assets/explosion.mp3")
    powerups.Bomb.countdown_sound = sound_effect("assets/bomb_countdown_beep.mp3")
    # Asteroid related sound effects
    asteroid.Asteroid.asteroid_split_sound = sound_effect("assets/orb.mp3")

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
    asteroidfield.AsteroidField.containers = (g["updatable"])
    asteroid.Asteroid.containers = (g["updatable"], g["drawable"], g["asteroids"])
    
    player.Player.containers = (g["updatable"], g["drawable"])
    player.ShieldPowerup.containers = (g["updatable"], g["drawable"], g["asteroid_interactors"])
    shot.Shot.containers = (g["updatable"], g["drawable"], g["asteroid_interactors"])
    
    powerups.Bomb.containers = (g["updatable"], g["drawable"], g["powerup_items"])
    powerups.BombExplosion.containers = (g["updatable"], g["drawable"], g["explosion_radii"])
    powerups.ShieldPowerupItem.containers = (g["updatable"], g["drawable"], g["powerup_items"])
    powerups.HealthPickup.containers = (g["updatable"], g["drawable"], g["powerup_items"])

def toggle_music() -> None:
    """Music on/off"""    
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()        
        return
    
    pygame.mixer.music.play(-1)