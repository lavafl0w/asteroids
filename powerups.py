import pygame
from circleshape import CircleShape
from constants import * #!

'''
bomb now needs to: register when player hits it and if so:
    start countdown, flashing each second
    after detonation, create new expanding circle that destroys asteroids

    if not activated, despawn
'''


class Bomb(CircleShape): #? OPTIMISE: Maybe have all the powerups pull from a powerup class
    def __init__(self, x:float, y:float) -> None:
        super().__init__(x, y, SHOT_RADIUS)
        self.detonate_timer = BOMB_DETONATE_TIME
        self.time_until_despawn = SPAWN_SECONDS
        self.activated = False
        self.width = 50
        self.height = 50
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

    def update_warning_flash(self, dt: float, color: str) -> None:
        self.color = color
        self.flash_timer += dt
         
        # Flash faster as the bomb gets closer to despawning.
        flash_interval = max(0.1, self.time_until_despawn / 10)
        if self.flash_timer >= flash_interval:
            self.visible = not self.visible
            self.flash_timer = 0.0

    def update(self, dt: float) -> None:
        if self.activated == False:
            self.time_until_despawn -= dt

            if self.time_until_despawn <= 0:
                self.kill()
                return

            if self.time_until_despawn > 5:
                self.color = "white"
                self.visible = True
                self.flash_timer = 0.0
                return

            self.update_warning_flash(dt, "yellow")
        
        elif self.activated == True:
            print("player_activated")
            if self.detonate_timer > 0:
                self.update_warning_flash(dt, "red")
                self.detonate_timer -= dt
                return
            print("detonate")
            self.detonate()
            
    def detonate(self) -> None:
        self.kill()
