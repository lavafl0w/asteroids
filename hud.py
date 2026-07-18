import pygame
from scorekeeper import ScoreKeeper

class HUD:
    def __init__(self):
        self.hud_surface:pygame.Surface = pygame.Surface((200, 50))
        self.hud_surface.fill("red")
        
