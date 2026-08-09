from typing import List, Literal
from pygame.event import Event
from core.audio_manager import audio
import pygame
import random

class PauseMenu:
    def __init__(self, screen:pygame.Surface) -> None:
        self.pause_screen = screen.copy()
        self.pause_screen.set_alpha(75)
        self.pause_screen.fill((8, 12, 22))
        self.title_font = pygame.font.Font("assets/fonts/orbitron/Orbitron-Bold.ttf", 60)
        self.subtitle_font = pygame.font.Font("assets/fonts/oxanium/Oxanium-Regular.ttf", 26)
        self.text_font = pygame.font.Font("assets/fonts/exo/Exo-Regular.ttf", 25)
        
        self.random_audio_selection = random.randint(1, 3)
        audio.pause_play_music()
        self.play_audio()
            
    def handle_events(self, events: List[Event]) -> None | Literal["game_loop"]:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                audio.pause_play_music()
                return "game_loop"
    
    def draw(self, screen: pygame.Surface) -> None:
        screen_rect = screen.get_rect()
        screen.blit(self.pause_screen, (0, 0))
        
        pause_title_surface = self.title_font.render("YOU HAVE PAUSED TIME! OMG!!", 1, "white")
        pause_title_rect = pause_title_surface.get_rect()
        pause_title_rect.center = (screen_rect.centerx, 80)
        screen.blit(pause_title_surface, pause_title_rect)
        
        pause_subtitle_surface = self.subtitle_font.render("Can't believe you figured out how to do something like that! :o", 1, "white")
        pause_subtitle_rect = pause_subtitle_surface.get_rect()
        pause_subtitle_rect.centerx = screen_rect.centerx
        pause_subtitle_rect.top = pause_title_rect.bottom + 10
        screen.blit(pause_subtitle_surface, pause_subtitle_rect)
        
        pause_sub_subtitle_surface = self.subtitle_font.render("You're amazing! :o", 1, "white")
        pause_sub_subtitle_rect = pause_sub_subtitle_surface.get_rect()
        pause_sub_subtitle_rect.centerx = screen_rect.centerx
        pause_sub_subtitle_rect.top = pause_subtitle_rect.bottom
        screen.blit(pause_sub_subtitle_surface, pause_sub_subtitle_rect)
                
        pause_text_surface = self.text_font.render("Press ESC to continue.", 1, "white")
        pause_text_rect = pause_text_surface.get_rect()
        pause_text_rect.centerx = screen_rect.centerx
        pause_text_rect.top = pause_sub_subtitle_rect.bottom + 50
        screen.blit(pause_text_surface, pause_text_rect)
    
    def update(self, dt:float) -> None:
        pass
    
    def play_audio(self) -> None:
        match self.random_audio_selection:
            case 1:
                audio.play_effect(audio.pause_game_1)
            case 2:
                audio.play_effect(audio.pause_game_2)
            case 3:
                audio.play_effect(audio.pause_game_3)