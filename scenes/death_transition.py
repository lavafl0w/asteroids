import pygame
from core.audio_manager import audio
from typing import Literal, List
from pygame.event import Event
from score_keeper import ScoreKeeper
from constants import SCREEN_WIDTH

class DeathTransition:
    def __init__(self, screen: pygame.Surface, death_audio_channel: pygame.mixer.Channel) -> None:
        self.fade_surface = screen.copy()
        self.fade_surface.set_alpha(0)
        self.fade_surface.fill((8, 12, 22))
        self.death_audio_channel = death_audio_channel
        self.max_fade_time = 5
        self.fade_time = 0
    
    def handle_events(self, events: List[Event]) -> None:
        pass
    
    def draw(self, screen:pygame.Surface) -> None:
        screen.blit(self.fade_surface, (0,0))
    
    def update(self, dt:float) -> None | Literal['damage_report']:
        # Switch music and wait until death effect is done
        if pygame.mixer.music.get_busy():
            audio.toggle_music()
        
        # Start fading the screen out/fade in the overlay
        if not self.death_audio_channel.get_busy():        
            # Increase how long we have been fading
            self.fade_time += dt
            
            # 0.0 - 1.0 factor for how long left to fade
            fade_progress = self.fade_time / self.max_fade_time
            fade_progress = min(1.0, max(fade_progress, 0.0))
            
            # Square the value to increase speed of fade
            curved_progress = fade_progress * fade_progress
            
            # Convert this to the calculated alpha (opacity) value
            alpha_value = curved_progress * 255
            self.fade_surface.set_alpha(int(alpha_value))
            
        if self.fade_time >= self.max_fade_time:
            return 'damage_report'

class DamageReport:
    '''This is the stats screen'''
    def __init__(self) -> None:
        self.title_font_obj = pygame.font.SysFont(None, 80)
        self.body_font_obj = pygame.font.SysFont(None, 36)
        self.background = (8, 12, 22)
        audio.start_music('damage_report')
        
    def handle_events(self, events: List[Event]) -> None | Literal['quit'] | Literal['game_loop_restart']:
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            return 'quit'
        elif keys[pygame.K_RETURN]:
            return 'game_loop_restart'
            
        
    def draw(self, screen:pygame.Surface) -> None:
        screen.fill(self.background)
        
        title_surface = self.title_font_obj.render("LMAO YOU DIED!", 1, "white")
        title_rect = title_surface.get_rect()
        title_rect.center = (SCREEN_WIDTH//2, 60)
        screen.blit(title_surface, title_rect)
        
        body_surface = self.body_font_obj.render("Press enter to respawn, ESC to quit.", 1, "white")
        body_rect = body_surface.get_rect()
        body_rect.center = (SCREEN_WIDTH//2, 200)
        screen.blit(body_surface, body_rect)
        
    def update(self, dt:float) -> None:
        pass