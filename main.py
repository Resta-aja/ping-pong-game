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

class ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.speed_x = player_speed
        self.speed_y = player_speed
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y < 0 or self.rect.y > win_heigth:
            self.speed_y *= -1
        

tenis_ball = ball(
    player_image='tenis_ball.png', 
    player_x=randint(275, 300), 
    player_y=400, 
    size_x=30, 
    size_y=30, 
    player_speed=3)


blue_racket = player(
    player_image='stick_tenis_biru.png', 
    player_x=20, 
    player_y=200, 
    size_x=80, 
    size_y=100, 
    player_speed=7)

red_racket = player(
    player_image='stick_tenis_merah.png', 
    player_x=600, 
    player_y=200, 
    size_x=80, 
    size_y=100, 
    player_speed=7)

game = True
finish = False
FPS = 60
clock = time.Clock()
font_style = font.SysFont('arial', 35)
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
        tenis_ball.reset()
        tenis_ball.update()

        if sprite.collide_rect(tenis_ball, red_racket) or sprite.collide_rect(tenis_ball, blue_racket):
            tenis_ball.speed_x *= -1

        if tenis_ball.rect.x > win_width:
            win_text = font_style.render('blue racket is the winner!!!',1,(39, 70, 226))
            window.blit(win_text, (200, 250))
            finish = True
        if tenis_ball.rect.x < 0:
            win_text = font_style.render('red racket is the winner!!!',1,(248, 13, 13))
            window.blit(win_text, (200, 250))
            finish = True
    display.update()
    clock.tick(FPS)