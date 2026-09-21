from dataclasses import dataclass
from constants import BASIC_ASTEROID_DESTOYED_SHOT_POINTS, BASIC_ASTEROID_SPLIT_SHOT_POINTS, BOMB_DESTROYED_POINTS, SHIELD_DESTROYED_POINTS

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
    shield_active: bool = False
    total_score: int = 0
    respawn_cost: int = 500 # How much respawning costs if player died

    def tick_time(self, dt:float) -> None:
        self.time_passed += dt
        
    def reset_time(self) -> None:
        self.time_passed = 0
        
    def player_respawn(self) -> None:
        self.reset_time()
        self.total_score -= self.respawn_cost

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
        
    def add_score(self, score_modifier_item: str | None = None) -> None:
        if score_modifier_item is None or score_modifier_item == "basic_kill":
            self.total_score += BASIC_ASTEROID_DESTOYED_SHOT_POINTS
        elif score_modifier_item == "asteroid_split":
            self.total_score += BASIC_ASTEROID_SPLIT_SHOT_POINTS
        elif score_modifier_item == "bomb_kill":
            self.total_score += BOMB_DESTROYED_POINTS
        elif score_modifier_item == "shield_kill":
            self.total_score += SHIELD_DESTROYED_POINTS

# Used to refer back to the same object to track updating values
ScoreKeeper = ScoreKeeperClass()