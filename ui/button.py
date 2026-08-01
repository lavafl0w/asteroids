import pygame
from pygame.event import Event
from typing import TypeVar, Generic, Callable
from core.audio_manager import audio

T = TypeVar("T")

class Button(Generic[T]):
    def __init__(self, width:int, height: int, centre:tuple, font_obj:pygame.font.Font,
                 button_text:str, base_color:str, hover_color:str, press_audio: pygame.mixer.Sound | None,
                 hover_audio: pygame.mixer.Sound | None,
                 callback: Callable[[], T]) -> None:
        self.button = pygame.Rect(0, 0, width, height)
        self.button.center = centre
        self.font = font_obj
        self.button_text = button_text
        self.base_color = base_color
        self.hover_color = hover_color
        self.press_audio = press_audio
        self.hover_audio = hover_audio
        self.audio_channel: pygame.mixer.Channel | None = None
        self.callback = callback
        self.hovered_over = False
        self.pending_callback = False
        
    def handle_events(self, event: Event) -> T | None:
        old_hover_state = self.hovered_over
        
        # If the mouse hovers over the button
        if event.type == pygame.MOUSEMOTION:
            self.hovered_over = self.button.collidepoint(event.pos)
            
        # If the button was pressed and was being hovered over
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered_over:
            
            self.audio_channel = audio.play_effect(self.press_audio) # Play press audio
            
            # If the audio was playing, then start pending for audio finish checks
            if self.audio_channel is not None: 
                self.pending_callback = True
                return
            
            # Guard against audio not being assigned, so just return immediately
            return self.callback()
        
        # If button isn't pending the callback and was just hovered over, play hover audio once
        if not self.pending_callback and (not old_hover_state and self.hovered_over):
            self.audio_channel = audio.play_effect(self.hover_audio)
    
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
        # If the channel was assigned, but is no longer busy and was actually also pending callback
        if self.audio_channel and not self.audio_channel.get_busy() and self.pending_callback == True:
            self.pending_callback = False # Reset values
            self.audio_channel = None
            return self.callback() # And return the callback

