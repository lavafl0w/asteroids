import pygame
from constants import SCREEN_WIDTH
from ui.button import Button
from typing import Literal
from core.audio_manager import audio

MainMenuAction = Literal['game_loop', 'quit']

class MainMenu:
    def __init__(self) -> None:
        self.title_font = pygame.font.Font(None, 64)
        self.button_font = pygame.font.Font(None, 32)
        self.menu_background = pygame.image.load("assets/amazing_menu_background.png")
        
        self.audio_channel: pygame.mixer.Channel | None = None
        
        self.start_button = Button(150, 75, (SCREEN_WIDTH/2, 350), self.button_font, 
                                    "Start Game", "red", "green", audio.menu_start_press_audio, audio.menu_start_hover_audio,
                                    self.start_game)
        self.quit_button = Button(150, 75, (SCREEN_WIDTH/2, 650), self.button_font, 
                                    "Quit", "red", "green", audio.menu_quit_press_audio, audio.menu_quit_hover_audio,
                                    self.quit_game)
                
    def handle_events(self, events) -> None | MainMenuAction:
        button_return = None
        if self.start_button.pending_callback or self.quit_button.pending_callback:
            return
        
        for event in events:
            button_return = self.start_button.handle_events(event)
            if button_return:
                return button_return

            button_return = self.quit_button.handle_events(event)
            if button_return:
                return button_return
            
    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.menu_background, (0,0))
        
        title_surface = self.title_font.render("ASTEROIDS", 1, "white")
        title_rect = title_surface.get_rect()
        title_rect.center = (int(SCREEN_WIDTH/2), 100)
        
        screen.blit(title_surface, title_rect)
        
        self.start_button.draw(screen)
        self.quit_button.draw(screen)
    
    def update(self, dt:float) -> None | MainMenuAction:      
        button_return = self.start_button.update()
        if button_return:
            return button_return
        
        button_return = self.quit_button.update()
        if button_return:
            return button_return
        
    
    def start_game(self) -> Literal['game_loop']:
        audio.start_music("game_loop") # Start music for game loop
        return "game_loop"
    
    def quit_game(self) -> Literal['quit']:
        return "quit"

