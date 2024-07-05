from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img ,cord_x ,cord_y ,width, height, speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_img),(width,height))
        self.rect = self.image.get_rect()
        self.rect.x = cord_x
        self.rect.y = cord_y
        self.speed = speed

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

player = GameSprite('platform.png',0,200,20,200,10)
enemy = GameSprite('enemy.png',650,200,50,200,10)
ball = GameSprite('ball.png',300,200,70,70,5)



speed_x = 4
speed_y = 4

score_player = 0
score_enemy = 0

font.init()
font1 = font.Font(None,35)


window = display.set_mode((700,500))
display.set_caption('ПИНГ-ПОНГ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

clock = time.Clock()

finish = False
game = True

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:

        window.fill( (255,255,255) )

        player.reset()
        enemy.reset()
        ball.reset()


        player_label = font1.render('Счет:' + str(score_player),1,(0,0,0))
        enemy_label = font1.render('Счет:' + str(score_enemy),1,(0,0,0))


        window.blit(player_label,(10,10))
        window.blit(enemy_label,(600,10))

        mouse_x, mouse_y = mouse.get_pos() 
        if player.rect.centery > mouse_y:
            player.rect.y -= 2
        else:
            player.rect.y += 2

        if enemy.rect.centery > ball.rect.centery:
            enemy.rect.y -= 2
        else:
            enemy.rect.y += 2

        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if sprite.collide_rect(ball,player) or sprite.collide_rect(ball,enemy):
            speed_x *= -1 
        if ball.rect.y < 0 or ball.rect.y > 430:
            speed_y *= -1


        if ball.rect.x < 0:
            score_enemy +=1
            ball.rect.x = 300

        if ball.rect.x > 630:
            score_player += 1
            ball.rect.x = 300    



    clock.tick(60)
    display.update()
