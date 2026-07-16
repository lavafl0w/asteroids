import pygame
import player, powerups, asteroid, asteroidfield, shot
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

def setup_pygame() -> tuple[pygame.Surface, pygame.time.Clock, pygame.font.Font]:
# Start Pygame instance, enables fonts and music
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
        
    # Set up font for display
    font = pygame.font.SysFont(None, 36)
    
    pygame_clock = pygame.time.Clock()
    
    screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    return screen, pygame_clock, font
    
    
def setup_audio() -> dict[str, pygame.mixer.Sound]:

    audio_dict = {}
    
    music = pygame.mixer.music
    music.load('assets/music_g_m.mp3')
    music.play(-1)
    
    audio_dict["music"] = music
    
    sound_effect = pygame.mixer.Sound
    
    player.Player.death_audio = sound_effect("assets/emotional_damage.mp3")
    #audio_dict["death_audio"] = sound_effect("assets/emotional_damage.mp3")
    
    powerups.Bomb.explosion_sound = sound_effect("assets/explosion.mp3")
    #audio_dict["bomb_explosion"] = sound_effect("assets/explosion.mp3")
    
    powerups.Bomb.tick_sound = sound_effect("assets/bomb_tick.mp3")
    #audio_dict["bomb_tick"] = sound_effect("assets/bomb_tick.mp3")
    
    asteroid.Asteroid.asteroid_split_sound = sound_effect("assets/orb.mp3")
    #audio_dict["asteroid_split"] = sound_effect("assets/orb.mp3")
    
    player.Player.shot_audio = sound_effect("assets/pew-pew-lame-sound-effect.mp3")
    
    return audio_dict

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
    
def assign_containers(g) -> None:
    
    asteroidfield.AsteroidField.containers = (g["updatable"]) # AstroidField class -> updatable
    player.Player.containers = (g["updatable"], g["drawable"]) # Player class -> updatable and drawable groups
    shot.Shot.containers = (g["updatable"], g["drawable"], g["shots"]) # Shot class -> updatable, drawable, shots
    asteroid.Asteroid.containers = (g["updatable"], g["drawable"], g["asteroids"]) # Astroid class -> updatable, drawable and asteroids
    powerups.Bomb.containers = (g["updatable"], g["drawable"], g["powerup_items"]) # Bomb class -> updatable, drawable, powerups
    powerups.BombExplosion.containers = (g["updatable"], g["drawable"], g["explosion_radii"])
