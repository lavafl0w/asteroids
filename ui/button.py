import pygame
from pygame.event import Event
from typing import TypeVar, Generic, Callable

T = TypeVar("T")

class Button(Generic[T]):
    def __init__(self, width:int, height: int, centre:tuple, font_obj:pygame.font.Font,
                 button_text:str, base_color:str, hover_color:str, press_audio: pygame.mixer.Sound | None,
                 hover_audio: pygame.mixer.Sound | None, audio_channel: pygame.mixer.Channel,
                 callback: Callable[[], T]) -> None:
        self.button = pygame.Rect(0, 0, width, height)
        self.button.center = centre
        self.font = font_obj
        self.button_text = button_text
        self.base_color = base_color
        self.hover_color = hover_color
        self.press_audio = press_audio
        self.hover_audio = hover_audio
        self.audio_channel = audio_channel
        self.callback = callback
        self.hovered_over = False
        self.pending_callback = False
        
    def handle_events(self, event: Event) -> T | None:
        old_hover_state = self.hovered_over
        
        if event.type == pygame.MOUSEMOTION:
            self.hovered_over = self.button.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered_over:
            if self.press_audio:
                self.audio_channel.play(self.press_audio) # Play press audio
                self.pending_callback = True
                return
            
            return self.callback() # Guard against audio not being assigned
        
        # If button isn't pending_callback was just hovered over, play hover audio once
        if self.hover_audio and not self.pending_callback and (not old_hover_state and self.hovered_over):
            self.audio_channel.play(self.hover_audio)
    
    def draw(self, screen:pygame.Surface) -> None:
        # Draw the overall/entire button rect coloured on screen
        colour = self.hover_color if self.hovered_over else self.base_color
        pygame.draw.rect(screen, colour, self.button)
        
        # Make the text surface, get the rect for it and position it in centre of button
        text_surface = self.font.render(self.button_text, 1, "white")
        text_rect = text_surface.get_rect()
        text_rect.center = self.button.center
        
        # Blit the text surface on the text rect
        screen.blit(text_surface, text_rect)
        
    def update(self) -> T | None:
        if not self.audio_channel.get_busy() and self.pending_callback == True:
            self.pending_callback = False
            return self.callback()

