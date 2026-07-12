import pygame
from circleshape import CircleShape
from constants import * #!

'''
bomb now needs to: register when player hits it and if so:
    start countdown, flashing each second (done)
    after detonation, create new expanding circle that destroys asteroids

    if not activated, despawn (done)
'''


class Bomb(CircleShape): #? OPTIMISE: Maybe have all the powerups pull from a powerup class
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
    def activate(self) -> None:
        self.activated = True
        self.time_until_despawn = 3
        print("item activated")

    # Helper for changing the color of the item and starting it flashing
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

            # Still got time left to collect
            if self.time_until_despawn > 5:
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
            
    def detonate(self) -> None:
        print("detonated")
        pygame.mixer.Sound("assets/explosion.mp3").play().set_volume(0.25)
        self.kill()
