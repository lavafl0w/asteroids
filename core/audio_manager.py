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
    # Pause
    pause_game_1: pygame.mixer.Sound | None = None
    pause_game_2: pygame.mixer.Sound | None = None
    pause_game_3: pygame.mixer.Sound | None = None
    
    def __init__(self) -> None:
        pass
    
    def setup_sound_effects(self) -> None:
        """Handles assigning sound effects"""    
        sound_effect = pygame.mixer.Sound

        # Player specific sound effect assignment
        self.player_death_audio = sound_effect("assets/audio/player/emotional_damage.mp3")
        self.player_shot_audio = sound_effect("assets/audio/bullets/pew_pew.mp3")
        self.player_hit_audio = sound_effect("assets/audio/player/player_hit_oof.mp3")
        self.player_low_health_audio = sound_effect("assets/audio/player/fable-health-low.mp3")
        # Health specific
        self.player_life_maximum_audio = sound_effect("assets/audio/health/maximum-patrona-lifes.mp3")
        self.player_life_pickup_audio = sound_effect("assets/audio/health/extra-lifee.mp3")
        # Start menu
        self.menu_start_hover_audio = sound_effect("assets/audio/main_menu/route_jingle.mp3")
        self.menu_quit_hover_audio = sound_effect("assets/audio/main_menu/bruh.mp3")
        self.menu_start_press_audio = sound_effect("assets/audio/main_menu/good_boy.mp3")
        self.menu_quit_press_audio = sound_effect("assets/audio/main_menu/vine_boom.mp3")
        # Shield
        self.shield_activate_effect = sound_effect("assets/audio/shield/shield_attacktivate.mp3")
        self.shield_deactivate_effect = sound_effect("assets/audio/shield/shield_pc-power-down.mp3")
        self.shield_break_effect = sound_effect("assets/audio/shield/shield_minecraft-glass-break.mp3")
        self.shield_hit_effect = sound_effect("assets/audio/shield/shield_tf2-critical-hit.mp3")
        # Bomb
        self.bomb_explosion_sound = sound_effect("assets/audio/bombs/explosion.mp3")
        self.bomb_countdown_sound = sound_effect("assets/audio/bombs/bomb_countdown_beep.mp3")
        # Asteroids
        self.asteroid_split_sound = sound_effect("assets/audio/asteroids/orb.mp3")
        # Pause
        self.pause_game_1 = sound_effect("assets/audio/scenes/pause/mincraft-villager-sound.mp3")
        self.pause_game_2 = sound_effect("assets/audio/scenes/pause/minecraft-2.mp3")
        self.pause_game_3 = sound_effect("assets/audio/scenes/pause/minecraft-3.mp3")

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
            music.load('assets/audio/music/music_san_andreas.mp3')
            music.set_volume(0.6)
            self.toggle_music()

        elif scene == "game_loop":
            music.load('assets/audio/music/music_glorious_morning.mp3')
            music.set_volume(0.4)
            self.toggle_music()
        
        elif scene == "damage_report":
            music.load('assets/audio/music/music_wii_menu.mp3')
            music.set_volume(0.2)
            self.toggle_music()
            
    def toggle_music(self) -> None:
        """Music on/off"""    
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()        
            return

        pygame.mixer.music.play(-1)
        
    def pause_play_music(self) -> None:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        
audio = AudioManager()