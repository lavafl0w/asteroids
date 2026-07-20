from dataclasses import dataclass, asdict

'''
This is the scorekeeping module. It keeps score of things (in both senses). It should keep track of things like:

Time played, asteroids destroyed (start with smallest first at least), total bullets fired, asteroids DECIMATED (where the bomb explosion has destroyed it), bombs activated/used, items picked up

There is also an actual score associated with some of these triggers, which on death returns the total score.

Some sort of respawn mechanic might be that on death, you can use a certain amount of your score to 'pay' for respawn. This value then increases depending on either the overall time played or number of times respawned. There would be a returned final score and a overall total score before being 'spent' to respawn.

Right now, focus on just tracking the values like time, bullets, asteroids, items
'''
# Made it a dataclass cause why not
# This sort just handles basically the __init__ part, automatically assigning the values like normal
# But converting 'time_passed' to 'self.time_passed'
@dataclass
class ScoreKeeperClass:
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
        
    #def get_score_keeper_values(self) -> dict[str, int | float]:
    #    return asdict(self) # Return all the attributes as a dictionary if needed

# Used to refer back to the same object to track updating values
ScoreKeeper = ScoreKeeperClass()