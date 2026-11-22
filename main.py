from pygame import *
from random import randint
from time import time as timer
font.init()
myfont = font.SysFont("monospace", 23)
mixer.init()
mixer.music.load("level/space.ogg")
mixer.music.play()
window = display.set_mode((700, 500))
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width,height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('level/bullet.png', self.rect.centerx, self.rect.top, 10, 15, 20)
        bullets.add(bullet)
lost = 0
kills = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80,620)
            lost+=1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        global kills
        if self.rect.y < 0:
            self.kill()


bullets = sprite.Group()
monsters = sprite.Group()
for i in range(5):
    enemy = Enemy('level/ufo.png', randint(80,620), 0, randint(1,5), 80, 50)
    monsters.add(enemy)
rocket = Player('level/rocket.png', 300, 400, 10, 80, 100)
background = transform.scale(image.load("level/galaxy.jpg"), (700, 500))
game = True
clock = time.Clock()
FPS = 60
finish = True
kick = mixer.Sound("level/fire.ogg")
kills = 0
myfont2 = font.SysFont("monospace", 50)
shoots = 0
start = timer()
reload = False
level = True
lifes = sprite.Group()
heart_x = 0
for i in range(3):
    life = GameSprite('level/heart.png', heart_x, 60, 10, 50, 50)
    lifes.add(life)
    heart_x+=30
while game:
    window.blit(background, (0, 0))
    label = myfont.render(f"Пропущено:{lost}", 1, (255, 255, 0))
    label2 = myfont.render(f"Убито:{kills}", 1, (255, 255, 0))
    window.blit(label, (0, 0))
    window.blit(label2, (0, 30))
    sprites_list = sprite.groupcollide(monsters, bullets, True, True)
    for b in sprites_list:
        kills += 1
        if level:
            enemy = Enemy('level/ufo.png', randint(80, 620), 0, randint(1, 5), 80, 50)
        else:
            enemy = Enemy('level/asteroid.png', randint(80, 620), 0, randint(5, 8), 80, 50)
        monsters.add(enemy)
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if shoots <5:
                    rocket.fire()
                    kick.play()
                    shoots += 1
                if shoots >= 5 and not(reload):
                    start = timer()
                    reload = True

    now = timer()
    if reload:
        if now - start >=3:
            shoots = 0
            reload = False
        else:
            label6 = myfont.render(f"перезарядка{round(now-start,1)}", 1, (0, 255, 0))
            window.blit(label6, (0, 100))
    if kills == 5 and level:
        level = False
        for monster in monsters:
            monster.kill()
        for i in range(5):
            enemy = Enemy('level/asteroid.png', randint(80, 620), 0, randint(5, 8), 80, 50)
            monsters.add(enemy)

    if kills >= 10:
        finish = False
        label3 = myfont2.render("YOU WIN", 1, (0, 255, 0))
        window.blit(label3, (200, 200))
    player_list = sprite.spritecollide(rocket, monsters, True)
    for i in player_list:
        lifes.sprites()[-1].kill()
        if level:
            enemy = Enemy('level/ufo.png', randint(80, 620), 0, randint(1, 5), 80, 50)
        else:
            enemy = Enemy('level/asteroid.png', randint(80, 620), 0, randint(5, 8), 80, 50)
        monsters.add(enemy)
    if lost >= 6 or len(lifes) == 0:
        finish = False
        label4 = myfont2.render("GAME OVER", 1, (255, 0, 0))
        window.blit(label4, (200, 200))

    if finish:
        rocket.update()
        rocket.reset()
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)
        lifes.update()
        lifes.draw(window)
    display.update()
    time.delay(FPS)