from pygame import *
from random import randint
init()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Ping-Pong")

background = transform.scale(
    image.load("lapanganpingpong.jpg"), (700, 500)
)

# ----------------- CLASS SPRITE -----------------
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_left(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < win_height - 100:
            self.rect.y += self.speed

    def update_right(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < win_height - 100:
            self.rect.y += self.speed

    def cpu_move(self, ball):
        # CPU cepat sejak level 1 — kejar bola secepatnya
        if ball.rect.centery < self.rect.centery:
            self.rect.y -= self.speed
        elif ball.rect.centery > self.rect.centery:
            self.rect.y += self.speed
        # Biar CPU gak keluar dari batas
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > win_height - 100:
            self.rect.y = win_height - 100

class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.speed_x = player_speed
        self.speed_y = player_speed

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.y < 0 or self.rect.y > win_height - 30:
            self.speed_y *= -1

# ----------------- SETUP OBJEK -----------------
tenis_ball = Ball('tenis_ball.png', 340, 250, 30, 30, 4)
blue_racket = Player('stick_tenis_biru.png', 20, 200, 80, 100, 7)
red_racket = Player('stick_tenis_merah.png', 600, 200, 80, 100, 7)

# ----------------- SETUP GAME -----------------
game = True
finish = False
menu = True
solo_mode = False
level = 1
max_level = 5

clock = time.Clock()
FPS = 60
font_style = font.SysFont('arial', 35)

# ----------------- FUNGSI RESET -----------------
def reset_positions():
    tenis_ball.rect.x = randint(275, 300)
    tenis_ball.rect.y = 250
    tenis_ball.speed_x = 4 + level
    tenis_ball.speed_y = 4 + level
    blue_racket.rect.y = 200
    red_racket.rect.y = 200

# ----------------- MENU MODE -----------------
while menu:
    window.blit(background, (0,0))
    text_title = font_style.render("Pilih Mode:", True, (255, 255, 255))
    solo_text = font_style.render("1 - Solo (Lawan CPU)", True, (255, 255, 0))
    duo_text = font_style.render("2 - Duo (2 Pemain)", True, (0, 255, 255))
    window.blit(text_title, (240, 150))
    window.blit(solo_text, (180, 250))
    window.blit(duo_text, (180, 300))
    display.update()

    for e in event.get():
        if e.type == QUIT:
            menu = False
            game = False
        if e.type == KEYDOWN:
            if e.key == K_1:
                solo_mode = True
                menu = False
            elif e.key == K_2:
                solo_mode = False
                menu = False

# ----------------- LOOP GAME -----------------
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN and finish:
            if e.key == K_r:
                finish = False
                reset_positions()
            if e.key == K_n and level < max_level:
                level += 1
                finish = False
                reset_positions()
            if e.key == K_BACKSPACE:
                game = False

    if not finish:
        window.blit(background, (0,0))
        blue_racket.reset()
        red_racket.reset()
        tenis_ball.reset()

        blue_racket.update_left()
        if solo_mode:
            red_racket.cpu_move(tenis_ball)
            red_racket.speed = 9 + level  # CPU cepat sejak awal, tambah cepat setiap level
        else:
            red_racket.update_right()

        tenis_ball.update()

        # Pantulan bola
        if sprite.collide_rect(tenis_ball, red_racket) or sprite.collide_rect(tenis_ball, blue_racket):
            tenis_ball.speed_x *= -1

        # Cek kalah/menang
        if tenis_ball.rect.x > win_width:
            win_text = font_style.render('Blue racket menang!', True, (39, 70, 226))
            window.blit(win_text, (200, 200))
            finish = True
        elif tenis_ball.rect.x < 0:
            win_text = font_style.render('Red racket menang!', True, (248, 13, 13))
            window.blit(win_text, (200, 200))
            finish = True

        # Level info
        level_text = font_style.render(f'Level: {level}', True, (255, 255, 255))
        window.blit(level_text, (10, 10))

    else:
        info_text = font_style.render("Tekan R untuk ulang, N untuk lanjut, BACKSPACE untuk keluar", True, (255, 255, 255))
        window.blit(info_text, (20, 300))

    display.update()
    clock.tick(FPS)
