
from pygame import *
from random import randint
mixer.init()
class GameSprite(sprite.Sprite):
    def __init__(self,image_name,player_x,player_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(image_name), (55,55))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        surface.blit(self.image,(self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT]and self.rect.x>5:
            self.rect.x -=self.speed
        if keys[K_RIGHT] and self.rect.x<win_width-80:
            self.rect.x +=self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx,self.rect.top, 15 )
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill    
win_width = 700
win_height = 500
surface = display.set_mode((win_width , win_height))
display.set_caption('zxc')
background = transform.scale(image.load('alban.jpg'),(win_width,win_height))
ship = Player('alban.jpg',5,420,10)
monsters = sprite.Group()
for i in range (1, 6):
    monster = Enemy('alban.jpg',randint(80,win_width),-50, randint(3,5) )
    monsters.add(monster)
asteroids = sprite.Group()
for i in range (1, 3):
    asteroid = Enemy('asteroid.png',randint(80,win_width),-50, 10 )
    asteroids.add(asteroid)
font.init()
font1 = font.Font(None,70)
font2 = font.Font(None,35)
win = font1.render('YOU WIN!', True, (255,255,0))
lose = font1.render('YOU LOSE!', True, (180,0,0))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
bullets = sprite.Group()
game = True
finish = False
clock = time.Clock()
FPS = 60
score = 0
lost = 0
goal = 10
max_lost = 20
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire.play()
                ship.fire()
                
        
    if finish != True:
        surface.blit(background, (0,0))
        text1 = font2.render('Пропущено:' + str(lost),1 ,(255,255,255))
        surface.blit(text1,(10,20))
        monsters.update()
        ship.update()
        ship.reset()
        monsters.draw(surface)
        asteroids.draw(surface)
        bullets.update()
        bullets.draw(surface)
        text2 = font2.render('Счет:' + str(score),1 ,(255,255,255))
        surface.blit(text2,(10,50))
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score +1
            monster = Enemy('alban.jpg',randint(80,win_width),-50, randint(3,5) )
            monsters.add(monster)
            print(score)
        if sprite.spritecollide(ship,monsters, False)or lost>= max_lost:
            finish = True
            surface.blit(lose,(200,200))
        if score >= goal:
            finish = True
            surface.blit(win,(200,200))
            
    display.update()
    clock.tick(FPS)
