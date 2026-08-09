from typing import List, Literal
from pygame.event import Event
from ui.button import Button
from core.audio_manager import audio
import pygame
import random

class PauseMenu:
    def __init__(self, screen:pygame.Surface) -> None:
        self.screen_rect = screen.get_rect()
        self.pause_screen_background = screen.copy()
        self.pause_screen_background.set_alpha(75)
        self.pause_screen_background.fill((8, 12, 22))
        self.title_font = pygame.font.Font("assets/fonts/orbitron/Orbitron-Bold.ttf", 60)
        self.subtitle_font = pygame.font.Font("assets/fonts/oxanium/Oxanium-Regular.ttf", 26)
        self.text_font = pygame.font.Font("assets/fonts/exo/Exo-Regular.ttf", 25)
        
        self.main_menu_button = Button(150, 75, (self.screen_rect.centerx, self.screen_rect.height * 2/3), self.text_font, 
                                    "Main Menu", "#722020", "green", audio.pause_menu_button_press, audio.pause_menu_button_hover,
                                    self.button_main_menu)
        
        self.random_audio_selection = random.randint(1, 3)
        audio.pause_play_music()
        self.play_audio()
            
    def handle_events(self, events: List[Event]) -> None | Literal["game_loop"] | Literal["main_menu"]:
        button_return = None
        if self.main_menu_button.pending_callback:
            return
        
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                audio.pause_play_music()
                return "game_loop"
            
            button_return = self.main_menu_button.handle_events(event)
            if button_return:
                return button_return
    
    def draw(self, screen: pygame.Surface) -> None:

        screen.blit(self.pause_screen_background, (0, 0))
        
        # Get each surface
        pause_title_surface = self.title_font.render("YOU HAVE PAUSED TIME! OMG!!", 1, "white")
        pause_subtitle_surface = self.subtitle_font.render("Can't believe you figured out how to do something like that! :o",1, "white")
        pause_sub_subtitle_surface = self.subtitle_font.render("You're amazing! :o", 1, "white")
        pause_text_surface = self.text_font.render("Press ESC to continue.", 1, "white")
        
        # Find the rects of all the surfaces
        pause_title_rect = pause_title_surface.get_rect()
        pause_subtitle_rect = pause_subtitle_surface.get_rect()
        pause_sub_subtitle_rect = pause_sub_subtitle_surface.get_rect()
        pause_text_rect = pause_text_surface.get_rect()
        
        # Get the total height of all the rects (and later also buffers) to vertically centre on screen
        total_base_rect_height = (pause_title_rect.height + pause_subtitle_rect.height +
                             pause_sub_subtitle_rect.height + pause_text_rect.height)
        total_rect_height = total_base_rect_height + 60 # This adds in the 10 / 50 pixel buffers
        
        # Position rects relative to title rect (which starts at the top of the total height)
        pause_title_rect.top = self.screen_rect.centery - total_rect_height // 2
        pause_title_rect.centerx = self.screen_rect.centerx
        
        pause_subtitle_rect.top = pause_title_rect.bottom + 10
        pause_subtitle_rect.centerx = self.screen_rect.centerx
        
        pause_sub_subtitle_rect.top = pause_subtitle_rect.bottom
        pause_sub_subtitle_rect.centerx = self.screen_rect.centerx
                
        pause_text_rect.top = pause_sub_subtitle_rect.bottom + 50
        pause_text_rect.centerx = self.screen_rect.centerx
        
        # Blit them all on screen
        screen.blit(pause_title_surface, pause_title_rect)
        screen.blit(pause_subtitle_surface, pause_subtitle_rect)
        screen.blit(pause_sub_subtitle_surface, pause_sub_subtitle_rect)
        screen.blit(pause_text_surface, pause_text_rect)
        
        self.main_menu_button.draw(screen, (self.screen_rect.centerx, pause_text_rect.bottom + 80))
    
    def update(self, dt:float) -> None | Literal['main_menu']:
        button_return = self.main_menu_button.update()
        if button_return:
            return button_return
    
    def play_audio(self) -> None:
        match self.random_audio_selection:
            case 1:
                audio.play_effect(audio.pause_game_1)
            case 2:
                audio.play_effect(audio.pause_game_2)
            case 3:
                audio.play_effect(audio.pause_game_3)
                
    def button_main_menu(self) -> Literal["main_menu"]:
        return "main_menu"