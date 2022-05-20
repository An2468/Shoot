from pygame import *
from random import randint
font.init()


window = display.set_mode((700, 600))

i = 0

clock = time.Clock()

display.set_caption("Space Thingy Shoot")

class ImageSprite(sprite.Sprite):
    def __init__(self, file, position, size, speed=(0, 0)):
        super().__init__()
        self.image = image.load(file)
        self.image = transform.scale(self.image, size)
        self.rect = Rect(position, size)
        self.speed = Vector2(speed)
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Player(ImageSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d]:
            self.rect.x += self.speed.x
        if keys[K_a]:
            self.rect.x -= self.speed.x
        
        if self.rect.right >= 700:
            self.rect.right = 700
        if self.rect.left <= 0:
            self.rect.left = 0
    def shoot(self):
        b = Bullet(file="bullet.png", position=self.rect.center, size=(20, 20), speed=(0, -30))
        bullets.add(b)

class Enemy(ImageSprite):
    def update(self):
        self.rect.topleft += self.speed
        if self.rect.bottom >= 600:
            self.rect.bottom = 0
            self.rect.x = randint(0, 600)
class Bullet(ImageSprite):
    def update(self):
        self.rect.topleft += self.speed
        if self.rect.top <= 0:
            self.kill()

class TextSprite(sprite.Sprite):
    def __init__(self, words, position, font_size, color):
        super().__init__()
        self.text = words
        self.position = position
        self.color = color
        self.font_size = font_size
        self.font = font.SysFont("Arial", 30)
        self.image = self.font.render(words, True, color)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
    def update_text(self, new_text):
        self.text = new_text
        self.image = self.font.render(self.text, True, self.color)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


enemies = sprite.Group()
for i in range(7):
    enemy = Enemy(file="ufo.png", position=(randint(0, 500), 0), size=(50, 40), speed=(0, randint(5, 10)))    
    enemies.add(enemy)

bullets = sprite.Group()


text = TextSprite(words="0", position = (0, 0), font_size=60, color=(255, 255, 255))
lives = TextSprite(words="lives: 3", position = (550, 0), font_size=60, color=(255, 255, 255))
rocket = Player(file="spaceship.png", position=(0, 510), size=(80, 80), speed=12.5)
background = Player(file="bg.png", position=(0, 0), size=(700, 600), speed=0)
enemy = Enemy(file="ufo.png", position=(0, 0), size=(100, 80), speed=(0, 2  ))
win_screen = Player(file="win.png", position=(0, 0), size=(700, 600), speed=0)
loose_screen = Player(file="looser.jpg", position=(0, 0), size=(700, 600), speed=0)

points = 0
live = 3

game_on = True

while game_on:

    for ev in event.get():

        if ev.type == QUIT:
            game_on = False
        if ev.type == KEYDOWN:
            if ev.key == K_SPACE:
                rocket.shoot()

    
    window.fill((255, 255, 255))
    background.update()
    background.draw(window)
    rocket.update()
    rocket.draw(window)
    enemies.update()
    enemies.draw(window)
    bullets.update()
    bullets.draw(window)
    text.draw(window)
    lives.draw(window)
    shots = sprite.groupcollide(bullets, enemies, True, True)
    if sprite.spritecollide(rocket, enemies, True):
        live = live - 1
        lives.update_text("live: " + str(live))
    if live <= 0:
        loose_screen.draw(window)


    for _ in shots:
        enemy = Enemy(file="ufo.png", position=(randint(0, 500), 0), size=(50, 40), speed=(0, randint(5, 10)))    
        enemies.add(enemy)
        points = points + 1
        text.update_text(str(points))
    if points >= 20:
        win_screen.draw(window)
    display.update()
    clock.tick(69)

    