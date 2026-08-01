from dataclasses import dataclass

# Made it a dataclass cause why not
# This sort just handles basically the __init__ part, automatically assigning the values like normal
# But converting 'time_passed' to 'self.time_passed' automatically outside of init
@dataclass
class ScoreKeeperClass:
    """This is the score keeping module. It keeps score (in both senses) of various stats, 
    and also the total score. This isn't fully fleshed out yet."""
    
    #NOTE: Currently has nothing in place for game_loop reset to wipe values
    time_passed: float = 0.0 # Time played
    bullets_fired:int = 0 # Total shots
    asteroids_shot:int = 0 # Total (small) asteroids destroyed by player shots
    asteroids_exploded:int = 0 # Total asteroids destroyed by bomb explosion
    items_picked_up:int = 0 # How many total items picked up // right now, this also includes bombs
    bombs_activated:int = 0 # How many bombs got activated
    player_lives: int = 0 # Current player lives

    def tick_time(self, dt:float) -> None:
        self.time_passed += dt

    def track_player_values(self, lives: int, shots: int) -> None:
        self.player_lives = lives
        self.bullets_fired = shots
        
    def asteroid_was_shot(self) -> None:
        self.asteroids_shot += 1
        
    def bomb_was_activated(self) -> None:
        self.bombs_activated += 1
        
    def asteroid_was_exploded(self) -> None:
        self.asteroids_exploded += 1
        
    def item_was_picked_up(self) -> None:
        self.items_picked_up += 1

# Used to refer back to the same object to track updating values
ScoreKeeper = ScoreKeeperClass()