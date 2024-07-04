from pygame import *
from random import randint
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img ,cord_x ,cord_y ,width, height,speed=5):
        super().__init__()
        self.image = transform.scale(image.load(sprite_img),(width,height))
        self.rect = self.image.get_rect()
        self.rect.x = cord_x
        self.rect.y = cord_y
        self.speed = speed
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 630:
            self.rect.x += 5
    def fire(self):
        bullet = Bullet('bullet.png',cord_x=self.rect.centerx,cord_y=self.rect.top,width=30,height=20,speed=20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update (self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0,600)
            lost += 1

class Bullet(GameSprite):
    def update (self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill
player = Player(sprite_img='rocket.png',cord_x=300,cord_y=400,width=70,height=100,speed=10)
enemys = sprite.Group()
bullets = sprite.Group()
for _ in range(5):
    enemy = Enemy('ufo.png',randint(0,600),0,100,100,randint(1,3)) 
    enemys.add(enemy)

# enemy = Enemy(sprite_img='ufo.png',cord_x=300,cord_y=0,width=100,height=100)
window = display.set_mode((700,500))
display.set_caption('Баку Гамасек трасуха')


background =  transform.scale(image.load('galaxy.jpg'),(700,500))

#mixer.init()
#mixer.load('music.mp3')
#mixer.music.play()
# fire_sound = mixer.Sound('fire.ogg')
font.init()
font1 = font.Font(None,35)
font2 = font.Font(None,100)


score = 0
lost = 0

clock = time.Clock()

finish = False

game = True

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
    if finish != True:

        window.blit(background,(0,0))

        player.reset()
        player.move()

        enemys.draw(window)
        enemys.update()

        bullets.draw(window)
        bullets.update()

        score_label = font1.render('Убито:'+ str(score),1,(255,255,255))
        lost_label = font1.render('Пропущенно:'+ str(lost),1,(255,255,255))
        # win_label = font2.render('Вы ПОБEДИЛИ!':'+ str(win),1,(0,255,50))
                    

        
        window.blit(score_label,(9,9))
        window.blit(lost_label,(9,40))

        if sprite.groupcollide(enemys,bullets,True,True):
            score += 1
        # enemy = Enemy('ufo.png',randint(0,600),0,100,100,randint(1,3)) 
        enemys.add(enemy)    

        if lost > 4:
            lose_label = font2.render('Вы Проиграли!',1,(255,0,50))
            window.blit(lose_label,(100,250))
            finish = True

        if score > 15:
            win_label = font2.render('Вы ПОБEДИЛИ!',1,(0,255,50))
            window.blit(win_label,(100,250))
            finish = True






    clock.tick(50)
    display.update()
    # baky lox😘

