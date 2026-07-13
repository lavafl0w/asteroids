import pygame
from circleshape import CircleShape
from constants import * #!
from logger import log_event

'''
bomb now needs to: register when player hits it and if so:
    start countdown, flashing each second (done)
    after detonation, create new expanding circle that destroys asteroids

    if not activated, despawn (done)
'''


class Bomb(CircleShape): # FUTURE: Maybe have all the powerups pull from a powerup class
    def __init__(self, x:float, y:float) -> None:
        super().__init__(x, y, SHOT_RADIUS)
        self.detonate_timer = BOMB_DETONATE_TIME
        self.time_until_despawn = TIME_UNTIL_ITEM_DESPAWN
        self.activated = False
        self.width = 40
        self.height = 25
        self.center = (int(x), int(y))
        self.color = "white"
        self.visible = True
        self.flash_timer = 0.0
        
    def draw_bomb(self) -> pygame.Rect:        
        bomb = pygame.Rect(0, 0, self.width, self.height)
        bomb.center = self.center
        return bomb
        
    def draw(self, screen: pygame.Surface) -> None:
        if self.visible:
            pygame.draw.rect(screen, self.color, self.draw_bomb())
    
    # Helper for item being activated and setting multiple variables
    # FUTURE: This would probably be included in powerup class
    def activate(self) -> None:
        self.activated = True
        self.time_until_despawn = 3
        print("item activated")

    # Helper for changing the color of the item and starts it flashing
    # FUTURE: This probably would be included in the class too
    def update_warning_flash(self, dt: float, color: str) -> None:
        self.color = color
        self.flash_timer += dt
         
        # Flash faster as the bomb gets closer to despawning.
        flash_interval = max(0.1, self.time_until_despawn / 10)
        if self.flash_timer >= flash_interval:
            self.visible = not self.visible
            self.flash_timer = 0.0

    def update(self, dt: float) -> None:
        # Item hasn't been activated yet
        if self.activated == False: 
            self.time_until_despawn -= dt # Remove time

            # Times up!
            if self.time_until_despawn <= 0:
                self.kill()
                return

            # Still got time left to pick it up
            if self.time_until_despawn > (TIME_UNTIL_ITEM_DESPAWN/2):
                self.color = "white"
                self.visible = True
                self.flash_timer = 0.0
                return

            # Getting closer, it's gonna despawn!
            self.update_warning_flash(dt, "yellow")
        
        # Let's blow something up!
        elif self.activated == True: 
            # Beep-Beep-Beep
            if self.detonate_timer > 0:
                self.update_warning_flash(dt, "red")
                self.detonate_timer -= dt
                return
            
            # Boom
            self.detonate()
    
    # How to boom        
    def detonate(self) -> None:
        log_event("bomb_detonated")
        pygame.mixer.Sound("assets/explosion.mp3").play().set_volume(0.20) # Make important boom noise
        self.kill() # Remove unexploded bomb
        BombExplosion(self.position.x, self.position.y, 1) # Start bomb explosion from where bomb was
        
# This handles creating the expanding explosion radius
class BombExplosion(CircleShape):
    def __init__(self, x:float, y:float, radius:float, time_alive:float = 0) -> None:
        super().__init__(x, y, radius)
        self.time_alive = time_alive # How long the explosion has been exploding for
        self.max_explosion_time = MAX_BOMB_EXPLOSION_TIME # How long can it explode for
        
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "red", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        #? This could maybe just be instead removing from max_time, rather than creating a whole new variable
        self.time_alive += dt # Increase how long the bomb has been active for
        
        # If the explosion hasn't finished yet
        #? and instead just be if max explosion is <= 0
        if self.time_alive <= self.max_explosion_time:
            # Make a new radius with basically the same params, but increase radius and pass in the cumulative
            # amount of time the explosion has been alive for
            BombExplosion(self.position.x, self.position.y, self.radius + 1, self.time_alive)    
        
        self.kill() # Kill this instance
        
        
