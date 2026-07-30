import pygame
from scorekeeper import ScoreKeeper

class HUD:
    def __init__(self) -> None:
        self.hud_surface:pygame.Surface = pygame.Surface((200, 150))
        self.hud_color = "black"
        self.hud_surface.fill(self.hud_color)
        self.lives_color = "white"
        self.previous_player_lives: int | None = None
        self.lives_change_time = 0
        self.font_object = pygame.font.SysFont(None, 26)
                
        # Create font object
        
    # Updates anything needed then draws
    def update_hud(self, dt:float) -> None:
        self.check_life_change(dt)
        self.draw_hud()
    
    def draw_hud(self) -> None:
        '''
        This draws all the text onto the HUD screen created at __init__, and after drawing onto the HUD
        screen that's attached to the class itself, the HUD screen gets blitted onto the main screen by main.py
        '''
           
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
            if index == 0: # If line 0 e.g 'Lives: ...'
                text_surface = self.font_object.render(line, 1, self.lives_color)
            else:
                text_surface = self.font_object.render(line, 1, "white")
                
            # Line 0 = (10, 10) -- Line 1 = (10, 10 + (1*25)) = (10, 35)
            position = (10, 10 + (index * 25)) 
            
            # Create a list of all the (text_surface, position) tuples
            blit_sequence.append((text_surface, position))
        
        # Draw the list of (surface, position) tuples onto the hud screen
        self.hud_surface.blits(blit_sequence)
        
    def check_life_change(self, dt:float) -> None:
        '''
        Checks the value of the player lives for if it had increased/decreased.
        Changes the colour of the text to green/red respectively for a short time.
        
        After couple seconds, goes back to white.
        '''
        # First check on run to assign previous values
        if self.previous_player_lives is None:
            self.previous_player_lives = ScoreKeeper.player_lives
            
        current_lives = ScoreKeeper.player_lives
        # Picked up life
        if current_lives > self.previous_player_lives:
            self.lives_color = "green"
            self.lives_change_time = 2    
        # Got hit
        elif current_lives < self.previous_player_lives:
            self.lives_color = "red"
            self.lives_change_time = 2
        
        # Colour change timer ran out
        if self.lives_change_time <= 0:
            self.lives_color = "white"
        
        # Sets new previous and decrements time
        self.previous_player_lives = current_lives
        self.lives_change_time -= dt