import pygame
from scorekeeper import ScoreKeeper

class HUD:
    def __init__(self, font_obj: pygame.font.Font) -> None:
        self.hud_surface:pygame.Surface = pygame.Surface((200, 150))
        self.hud_color = "black"
        self.hud_surface.fill(self.hud_color)
        #self.time_played = 0
        #self.bullets_shot = 0
        self.font_object = font_obj
        
    # Retrieve values from ScoreKeeper, updates then draws
    def update_hud(self) -> None:
        #self.player_lives = ScoreKeeper.player_lives
        #self.bullets_shot = ScoreKeeper.bullets_fired
        
        self.draw_hud()
        
    # Draws HUD values onto HUD screen, which then gets blitted by main.py
    def draw_hud(self) -> None:
        # Wipe the HUD screen before a new draw
        self.hud_surface.fill(self.hud_color)
        blit_sequence = []
        
        # All the text lines to be displayed
        hud_lines = [
            f"Lives: {ScoreKeeper.player_lives}",
            f"Bullets Fired: {ScoreKeeper.bullets_fired}",
            f"Asteroids Destroyed: {ScoreKeeper.asteroids_shot}"
        ]
        
        # For each line, create the text surface, and increase position by 20y per index
        for index, line in enumerate(hud_lines):
            text_surface = self.font_object.render(line, 1, "white")
            
            # Line 0 = (10, 10) -- Line 1 = (10, 10 + (1*25)) = (10, 35)
            position = (10, 10 + (index * 25)) 
            
            # Create a list of surface, position tuples
            blit_sequence.append((text_surface, position))
        
        # Draw the list of (surface, position) tuples onto the hud screen
        self.hud_surface.blits(blit_sequence)