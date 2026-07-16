import pygame
from scorekeeper import ScoreKeeper

class HUD:
    #hud_surface = pygame.Surface((300, 150))
    def __init__(self):
        self.hud_surface:pygame.Surface = pygame.Surface((300, 150))
        self.hud_surface.fill("red")
