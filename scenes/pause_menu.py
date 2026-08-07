from typing import List, Literal
from pygame.event import Event
from core.audio_manager import audio
import pygame
import random

class PauseMenu:
    def __init__(self, screen:pygame.Surface):
        self.pause_screen = screen.copy()
        self.pause_screen.set_alpha(75)
        self.pause_screen.fill((8, 12, 22))
        self.font_obj = pygame.font.SysFont(None, 72)
        self.random_audio_selection = random.randint(1, 3)
        audio.pause_play_music()
        self.play_audio()
            
    def handle_events(self, events: List[Event]) -> None | Literal["game_loop"]:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                audio.pause_play_music()
                return "game_loop"
    
    def draw(self, screen: pygame.Surface):
        screen_rect = screen.get_rect()
        
        screen.blit(self.pause_screen, (0, 0))
        
        pause_surface = self.font_obj.render("PAUSEDDDDDDDDDDDD", 1, "white")
        pause_rect = pause_surface.get_rect()
        pause_rect.center = screen_rect.center
        
        screen.blit(pause_surface, pause_rect)
    
    def update(self, dt:float):
        pass
    
    def play_audio(self):
        match self.random_audio_selection:
            case 1:
                audio.play_effect(audio.pause_game_1)
            case 2:
                audio.play_effect(audio.pause_game_2)
            case 3:
                audio.play_effect(audio.pause_game_3)