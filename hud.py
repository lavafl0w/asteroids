import pygame
from score_keeper import ScoreKeeper
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

class HUD:
    def __init__(self, screen: pygame.Surface, player) -> None:
        self.main_screen: pygame.Surface = screen
        self.lower_hud_surface:pygame.Surface = pygame.Surface((SCREEN_WIDTH, 50))
        self.shield_hud_surface: pygame.Surface = pygame.Surface((200, 150))
        self.shield_hud_rect = self.shield_hud_surface.get_rect()
        #self.shield_hud_rect.center = (SCREEN_WIDTH // 2, self.shield_hud_rect.height // 2)
        self.shield_hud_color = "red"
        self.lower_hud_color = "black"
        self.lower_hud_surface.fill(self.lower_hud_color)
        self.lower_hud_rect = self.lower_hud_surface.get_rect()
        self.player = player
        self.lives_color = "white"
        self.previous_player_lives: int | None = None
        self.lives_change_time = 0
        self.font_object = pygame.font.SysFont(None, 26)
        self.total_elapsed_seconds = 0
        self.shield_active = False
        self.shield_hits_remain = 0
        self.shield_time_remain = 0
    
    def update_hud(self, dt:float) -> None:
        self.check_life_change(dt)
        self.total_elapsed_seconds = int(ScoreKeeper.time_passed)
        self.check_shield_info()

    def draw_hud(self) -> None:
        self.draw_lower_hud()
        if self.shield_active:
            self.draw_shield_hud()
    
    def draw_lower_hud(self) -> None:
        """This draws all the text onto the HUD screen created at __init__, and after drawing onto the HUD
        screen that's attached to the class itself, the HUD screen gets blitted onto the main screen by main.py"""
           
        # Wipe the HUD screen before a new draw
        self.lower_hud_surface.fill(self.lower_hud_color)
        blit_sequence = []
        
        minutes_elapsed, seconds_elapsed = divmod(self.total_elapsed_seconds, 60)
        
        # All the text lines to be displayed
        hud_lines = [
            f"Time Elapsed: {minutes_elapsed}:{seconds_elapsed:02}",
            f"Lives: {ScoreKeeper.player_lives}",
            f"Score: xxxxxx",
            #f"Bullets Fired: {ScoreKeeper.bullets_fired}",
            #f"Asteroids Destroyed: {ScoreKeeper.asteroids_shot}", 
            #f"Shield {self.shield_active} -- hits: {self.shield_hits_remain} -- time: {self.shield_time_remain}"
        ]
        
        # Split the hud into even segments
        hud_segment = self.lower_hud_rect.width / len(hud_lines)
        
        # For each line, create the text surface, and increase position by 20y per index
        for index, line in enumerate(hud_lines):
            if index == 1: # If line 1 e.g 'Lives: ...'
                text_surface = self.font_object.render(line, 1, self.lives_color)
            else:
                text_surface = self.font_object.render(line, 1, "white")
            
            # Create a rect based off this lines hud segment
            segment_rect = pygame.Rect(
                hud_segment * index,
                0,
                hud_segment,
                self.lower_hud_rect.height
            )
                
            # Get the rect of the variable sized text, positioned in the centre of the segement
            text_rect = text_surface.get_rect(center = segment_rect.center)    
            
            # Position for text is (x, y) == (text.left, text.top)
            # (Since position is worked out based on top left corner)
            position = (text_rect.left, text_rect.top) 
            
            # Create a list of all the (text_surface, position) tuples
            blit_sequence.append((text_surface, position))
        
        # Draw the list of (surface, position) tuples onto the hud screen
        self.lower_hud_surface.blits(blit_sequence)
        
        self.main_screen.blit(self.lower_hud_surface, (0,SCREEN_HEIGHT - 50))
        
    def check_life_change(self, dt:float) -> None:
        """Checks the value of the player lives for if it had increased/decreased.
        Changes the colour of the text to green/red respectively for a short time.
        
        After couple seconds, goes back to white."""
        
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
        
    def check_shield_info(self):
        self.shield_active = True if self.player.active_shield else False
        
        if self.player.active_shield is not None:
            self.shield_hits_remain = self.player.active_shield.shield_hits_remaining
            self.shield_time_remain = int(self.player.active_shield.shield_time_remaining)
        else:
            self.shield_hits_remain = 0
            self.shield_time_remain = 0
            
    def draw_shield_hud(self):
        self.shield_hud_surface.fill(self.shield_hud_color) # Currently red for testing
        
        shield_title_surface = self.font_object.render("SHIELD ACTIVATED", 1, "orange")
        shield_title_rect = shield_title_surface.get_rect()
        shield_title_rect.center = (self.shield_hud_rect.width // 2, self.shield_hud_rect.height // 6)
        self.shield_hud_surface.blit(shield_title_surface, shield_title_rect)
        
        stat_hits_surface = self.font_object.render(f"Hits Remaining: {self.shield_hits_remain}", 1, "orange")
        stat_hit_rect = stat_hits_surface.get_rect()
        stat_hit_rect.center = (self.shield_hud_rect.width // 2, (self.shield_hud_rect.height // 6)*3)
        self.shield_hud_surface.blit(stat_hits_surface, stat_hit_rect)
        
        stat_time_surface = self.font_object.render(f"Time Remaining: {self.shield_time_remain}", 1, "orange")
        stat_time_rect = stat_time_surface.get_rect()
        stat_time_rect.center = (self.shield_hud_rect.width // 2, (self.shield_hud_rect.height // 6)*5)
        self.shield_hud_surface.blit(stat_time_surface, stat_time_rect)
        
        self.shield_hud_rect.center = (SCREEN_WIDTH // 2, self.shield_hud_rect.height // 2)
        self.main_screen.blit(self.shield_hud_surface, self.shield_hud_rect)