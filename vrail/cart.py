import math

import pygame


from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN
)

class Cart(pygame.sprite.Sprite):
    def __init__(self,SCREEN_WIDTH, SCREEN_HEIGHT):
        super(Cart, self).__init__()
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.surf = pygame.Surface((75, 25))
        self.surf.set_colorkey( (0,0,0) )
        self.surf.fill((255, 255, 255))
        pygame.draw.lines(self.surf, (0, 0, 255), False,
                          [(40,12),(55,12), (50,17),(55,12), (50,7) ])
        self.rect = self.surf.get_rect()
        self.drive = False


    def update(self, pressed_keys):
        self.handle_keys(pressed_keys)
        self.keep_player_on_screen()

    def handle_keys(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

    def keep_player_on_screen(self):
       if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.SCREEN_WIDTH:
            self.rect.right = self.SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= self.SCREEN_HEIGHT:
            self.rect.bottom = self.SCREEN_HEIGHT





    def set_pos(self,pos,pos1):

        self.target = pos1
        self.rect.left = pos[0] - self.rect.width/2
        self.rect.top = pos[1] - self.rect.height/2

        angle_rad = math.atan ( (pos[1] - pos1[1]) /(pos[0] - pos1[0])) * -1
        angle = math.degrees(  angle_rad )

        self.surf = pygame.transform.rotate(self.surf, angle)

    def toggle_drive(self):
        self.drive = not self.drive
