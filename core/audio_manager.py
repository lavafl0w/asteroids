import pygame

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
    
    def __init__(self) -> None:
        pass
    
    def setup_sound_effects(self) -> None:
        """Handles assigning sound effects"""    
        sound_effect = pygame.mixer.Sound

        # Player specific sound effect assignment
        self.player_death_audio = sound_effect("assets/emotional_damage.mp3")
        self.player_shot_audio = sound_effect("assets/pew_pew.mp3")
        self.player_hit_audio = sound_effect("assets/player_hit_oof.mp3")
        self.player_low_health_audio = sound_effect("assets/fable-health-low.mp3")
        # Health specific
        self.player_life_maximum_audio = sound_effect("assets/maximum-patrona-lifes.mp3")
        self.player_life_pickup_audio = sound_effect("assets/extra-lifee.mp3")
        # Start menu
        self.menu_start_hover_audio = sound_effect("assets/route_jingle.mp3")
        self.menu_quit_hover_audio = sound_effect("assets/bruh.mp3")
        self.menu_start_press_audio = sound_effect("assets/good_boy.mp3")
        self.menu_quit_press_audio = sound_effect("assets/vine_boom.mp3")
        # Shield
        self.shield_activate_effect = sound_effect("assets/shield_attacktivate.mp3")
        self.shield_deactivate_effect = sound_effect("assets/shield_pc-power-down.mp3")
        self.shield_break_effect = sound_effect("assets/shield_minecraft-glass-break.mp3")
        self.shield_hit_effect = sound_effect("assets/shield_tf2-critical-hit.mp3")
        # Bomb
        self.bomb_explosion_sound = sound_effect("assets/explosion.mp3")
        self.bomb_countdown_sound = sound_effect("assets/bomb_countdown_beep.mp3")
        # Asteroids
        self.asteroid_split_sound = sound_effect("assets/orb.mp3")

    def play_effect(self, sound_effect:pygame.mixer.Sound | None) -> pygame.mixer.Channel | None:
        """Plays the passed in sound effect, returns the channel it's playing on."""
        #TODO if sound effect name does not exist, error
            
        if sound_effect is not None:
            channel = sound_effect.play()
            return channel
        
        raise TypeError("Sound effect has not been assigned", sound_effect)
        
    def start_music(self, scene) -> None:
        """Load music for scene and play"""
        music = pygame.mixer.music

        if music.get_busy():
            self.toggle_music()
            music.unload()

        if scene == "main_menu":
            music.load('assets/music_san_andreas.mp3')
            music.set_volume(0.6)
            self.toggle_music()

        elif scene == "game_loop":
            music.load('assets/music_glorious_morning.mp3')
            music.set_volume(0.4)
            self.toggle_music()
            
    def toggle_music(self) -> None:
        """Music on/off"""    
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()        
            return

        pygame.mixer.music.play(-1)
        
audio = AudioManager()