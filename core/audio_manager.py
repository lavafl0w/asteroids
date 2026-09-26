import pygame
import logging

from pygame.mixer import Sound

logger = logging.getLogger("asteroids")

class AudioManager:
    # Player specific sound effects
    player_death_audio: pygame.mixer.Sound | None = None
    player_shot_audio: pygame.mixer.Sound | None = None
    player_hit_audio: pygame.mixer.Sound | None = None
    player_low_health_audio: pygame.mixer.Sound | None = None
    # Player health
    player_life_pickup_audio: pygame.mixer.Sound | None = None
    player_life_maximum_audio: pygame.mixer.Sound | None = None
    # Start menu
    menu_start_hover_audio: pygame.mixer.Sound | None = None
    menu_quit_hover_audio: pygame.mixer.Sound | None = None
    menu_start_press_audio: pygame.mixer.Sound | None = None
    menu_quit_press_audio: pygame.mixer.Sound | None = None
    # Shield
    shield_activate_effect: pygame.mixer.Sound | None = None
    shield_deactivate_effect: pygame.mixer.Sound | None = None
    shield_hit_effect: pygame.mixer.Sound | None = None
    shield_break_effect: pygame.mixer.Sound | None = None
    # Bomb
    bomb_explosion_sound: pygame.mixer.Sound | None = None
    bomb_countdown_sound: pygame.mixer.Sound | None = None
    # Asteroid
    asteroid_split_sound: pygame.mixer.Sound | None = None
    # Pause
    pause_game_1: pygame.mixer.Sound | None = None
    pause_game_2: pygame.mixer.Sound | None = None
    pause_game_3: pygame.mixer.Sound | None = None
    pause_menu_button_hover: pygame.mixer.Sound | None = None
    pause_menu_button_press: pygame.mixer.Sound | None = None
    # Rapid Fire
    rapid_fire_activate: pygame.mixer.Sound | None = None
    rapid_fire_shot: pygame.mixer.Sound | None = None
    # Damage Report
    player_respawn: pygame.mixer.Sound | None = None
    player_poor_respawn: pygame.mixer.Sound | None = None
    
    def __init__(self) -> None:
        pass
    
    def setup_sound_effects(self) -> None:
        """Handles assigning sound effects"""    
        # Player specific sound effect assignment
        self.player_death_audio = self.load_sound("assets/audio/player/emotional_damage.mp3")
        self.player_shot_audio = self.load_sound("assets/audio/bullets/pew_pew.mp3", 0.5)
        self.player_hit_audio = self.load_sound("assets/audio/player/player_hit_oof.mp3")
        self.player_low_health_audio = self.load_sound("assets/audio/player/fable-health-low.mp3")
        # Health specific
        self.player_life_maximum_audio = self.load_sound("assets/audio/health/maximum-patrona-lifes.mp3", 0.5)
        self.player_life_pickup_audio = self.load_sound("assets/audio/health/extra-lifee.mp3", 0.7)
        # Start menu
        self.menu_start_hover_audio = self.load_sound("assets/audio/main_menu/route_jingle.mp3", 0.4)
        self.menu_quit_hover_audio = self.load_sound("assets/audio/main_menu/bruh.mp3", 0.25)
        self.menu_start_press_audio = self.load_sound("assets/audio/main_menu/good_boy.mp3")
        self.menu_quit_press_audio = self.load_sound("assets/audio/main_menu/vine_boom.mp3")
        # Shield
        self.shield_activate_effect = self.load_sound("assets/audio/shield/shield_attacktivate.mp3")
        self.shield_deactivate_effect = self.load_sound("assets/audio/shield/shield_pc-power-down.mp3")
        self.shield_break_effect = self.load_sound("assets/audio/shield/shield_minecraft-glass-break.mp3")
        self.shield_hit_effect = self.load_sound("assets/audio/shield/shield_tf2-critical-hit.mp3", 0.5)
        # Bomb
        self.bomb_explosion_sound = self.load_sound("assets/audio/bombs/explosion.mp3")
        self.bomb_countdown_sound = self.load_sound("assets/audio/bombs/bomb_countdown_beep.mp3", 0.5)
        # Asteroids
        self.asteroid_split_sound = self.load_sound("assets/audio/asteroids/orb.mp3", 0.5)
        # Pause
        self.pause_game_1 = self.load_sound("assets/audio/pause_menu/mincraft-villager-sound.mp3")
        self.pause_game_2 = self.load_sound("assets/audio/pause_menu/minecraft-2.mp3")
        self.pause_game_3 = self.load_sound("assets/audio/pause_menu/minecraft-3.mp3")
        self.pause_menu_button_hover = self.load_sound("assets/audio/pause_menu/beep-select.mp3", 0.6)
        self.pause_menu_button_press = self.load_sound("assets/audio/pause_menu/noob.mp3")
        # Rapid Fire
        self.rapid_fire_activate = self.load_sound("assets/audio/rapid_fire/suppressing-fire.mp3", 0.4)
        self.rapid_fire_shot = self.load_sound("assets/audio/rapid_fire/rapid-fire-shot.mp3", 0.3)
        # Damage Report
        self.player_respawn = self.load_sound("assets/audio/other/chaching.mp3")
        self.player_poor_respawn = self.load_sound("assets/audio/other/help-me-im-poor.mp3")
            
        logger.info("SFX setup complete")
        
    def load_sound(self, file_path, volume = 1.0) -> Sound | None:
        """Tries to load the sound effect and handles any issues"""
        sound_effect = pygame.mixer.Sound
        loaded_effect = None
        
        try:
            loaded_effect = sound_effect(file_path)
            loaded_effect.set_volume(volume)
        except FileNotFoundError:
            logger.warning(f"File path not found: ({file_path})... continuing...")
                
        return loaded_effect
            
    def play_effect(self, sound_effect:pygame.mixer.Sound | None) -> pygame.mixer.Channel | None:
        """Plays the passed in sound effect, returns the channel it's playing on."""            
        if sound_effect is not None:
            channel = sound_effect.play()
            return channel
        else:
            logger.warning(f"This sound effect has not been assigned!")
            return None
        
    def start_music(self, scene) -> None:
        """Load music for scene and play"""
        music = pygame.mixer.music

        if music.get_busy():
            self.toggle_music()
            music.unload()

        if scene == "main_menu":
            music.load('assets/audio/music/music_san_andreas.mp3')
            music.set_volume(0.3)
            self.toggle_music()
            logger.info("Main menu music started!")

        elif scene == "game_loop":
            music.load('assets/audio/music/music_glorious_morning.mp3')
            music.set_volume(0.25)
            self.toggle_music()
            logger.info("Game loop music started!")
        
        elif scene == "damage_report":
            music.load('assets/audio/music/music_wii_menu.mp3')
            music.set_volume(0.2)
            self.toggle_music()
            logger.info("Death screen music started!")
            
    def toggle_music(self) -> None:
        """Music on/off"""    
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            logger.info("Music stopped")        
            return

        pygame.mixer.music.play(-1)
        
    def pause_play_music(self) -> None:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            logger.info("Music paused")
        else:
            pygame.mixer.music.unpause()
            logger.info("Music resumed")
        
audio = AudioManager()