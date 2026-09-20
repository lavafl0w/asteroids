import random
from constants import (HEALTH_SPAWN_CHANCE, SHIELD_SPAWN_CHANCE, BOMB_SPAWN_CHANCE, RAPID_FIRE_SPAWN_CHANCE)
from powerups.bomb import Bomb
from powerups.pickups import ShieldPowerupItem, HealthPickup, RapidFirePickup

def check_powerup_drop(asteroid_position) -> None:
    '''
    This decides if a powerup should drop based on simple table roll.
    
    item_1 = bomb
    item_2 = shield
    item_3 = health
    item_4 = rapid_fire
    
    Leaving a 30% chance for any item to spawn, each weighted the same at 10 right now.
    '''
    
    roll = random.randrange(0, 100)
    item_1_chance = BOMB_SPAWN_CHANCE  # 10
    item_2_chance = item_1_chance + SHIELD_SPAWN_CHANCE  # 10+10 = 20
    item_3_chance = item_2_chance + HEALTH_SPAWN_CHANCE  # 20+10 = 30
    item_4_chance = item_3_chance + RAPID_FIRE_SPAWN_CHANCE # 30+10 = 40
    
    if roll < item_1_chance:  # 0-10
        Bomb(asteroid_position.x, asteroid_position.y)
    elif roll < item_2_chance:  # 10-20
        ShieldPowerupItem(asteroid_position.x, asteroid_position.y)
    elif roll < item_3_chance:  # 20-30
        HealthPickup(asteroid_position.x, asteroid_position.y)
    elif roll < item_4_chance:  # 30-40
        RapidFirePickup(asteroid_position.x, asteroid_position.y)