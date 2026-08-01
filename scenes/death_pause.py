import pygame
from core.audio_manager import audio
from typing import Literal, List
from pygame.event import Event

class DeathPause:
    def __init__(self, death_audio_channel: pygame.mixer.Channel) -> None:
        self.death_audio_channel = death_audio_channel
    
    def handle_events(self, events: List[Event]) -> None:
        pass
    
    def draw(self, screen:pygame.Surface) -> None:
        #TODO: Temporary death pause screen visual, need to design
        screen.fill("red")
    
    def update(self, dt:float) -> None | Literal['quit']:
        # Switch music and wait until death effect is done
        if pygame.mixer.music.get_busy():
            audio.toggle_music()
        
        if not self.death_audio_channel.get_busy():        
            return "quit"
        