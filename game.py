# Импорт pygame
from pygame import *
# 
window = display.set_mode((700,500))

background = image.load('background1.jpg')
background = transform.scale(background,(700,500))

hitler = transform.scale(image.load('hitler.png'),(100,100))
pikachu = transform.scale (image.load('pikachu.png'),(100,100))

pikachu_x, pikachu_y = 100,200
hitler_x,hitler_y = 200,300

end = 0

game = True
while game:

    window.blit(background,(0,0))
    window.blit(hitler,(hitler_x,hitler_y))
    window.blit(pikachu,(pikachu_x,pikachu_y))
    for game_event in event.get():
        if game_event.type == QUIT:
            game = False

    keys = key.get_pressed()
    if keys [K_w]:
        hitler_y -= 5
    if keys [K_s]:
        hitler_y += 5
    if keys [K_d]:
        hitler_x += 5
    if keys [K_a]:
        hitler_x -= 5
    if hitler_x < pikachu_x:
        pikachu_x -15
    else:
        pikachu_x += 1   
    if hitler_y < pikachu_y:
        pikachu_y-=1
    else:
        pikachu_y += 1

    end += 20
    if end > 10000:
        print("ПОБЕДА РЕЙХА")
        game = False
    time.delay(20)
    display.update() 

        