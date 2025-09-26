from pygame import *
from random import randint
init()

win_width = 700
win_heigth = 500
window = display.set_mode((win_width,win_heigth))
display.set_caption("Ping-Pong")

background = transform.scale(
    image.load("lapanganpingpong.jpg"), (700,500)
)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class player(GameSprite):
    def update_left(self):
        #utk mengendalikan player
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y>0:
            self.rect.y-=self.speed
        if keys_pressed[K_s] and self.rect.y<450:
            self.rect.y+=self.speed
        
    def update_right(self):
        #utk mengendalikan player
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and self.rect.y>0:
            self.rect.y-=self.speed
        if keys_pressed[K_DOWN] and self.rect.y<450:
            self.rect.y+=self.speed

blue_racket = player(
    player_image='stick_tenis_biru.png', 
    player_x=20, 
    player_y=400, 
    size_x=80, 
    size_y=100, 
    player_speed=7)

red_racket = player(
    player_image='stick_tenis_merah.png', 
    player_x=600, 
    player_y=400, 
    size_x=80, 
    size_y=100, 
    player_speed=7)

game = True
finish = False
FPS = 60
clock = time.Clock()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        window.blit(background, (0,0))
        blue_racket.reset()
        blue_racket.update_left()
        red_racket.reset()
        red_racket.update_right()

    display.update()
    clock.tick(FPS)