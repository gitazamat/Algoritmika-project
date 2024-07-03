from pygame import *
 
class GameSprite(sprite.Sprite):
    def __init__(self , img , x , y):
        super().__init__()
        self.image = transform.scale(image.load(img),(60,60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self): 
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= 5    
        if keys[K_s] and self.rect.y < 440:
            self.rect.y += 5
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= 5
        if keys[K_d] and self.rect.x < 640:
            self.rect.x += 5    

class Enemy(GameSprite):

    def move(self):
        if self.rect.x <= 500:
            self.side = 'Right'
        if self.rect.x >= 640:
            self.side = 'Left'

        if self.side == 'Left':
            self.rect.x -= 5
        else:
            self.rect.x += 5
class Wall(sprite.Sprite):
    def __init__(self,x,y,w,h):
        super().__init__()
        self.width = w
        self.height = h
        self.wall = Surface((self.width,self.height))
        self.wall.fill((87, 239, 67))
        self.rect = self.wall.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self): 
        window.blit(self.wall,(self.rect.x,self.rect.y))

wall_1 = Wall(20,20,20,500)
player = Player('hero.png',300,300)
enemy = Enemy('cyborg.png',350,200)
treasure = GameSprite('treasure.png',600,400)


window = display.set_mode((700,500))
display.set_caption('Maze Game')

background =  transform.scale(image.load('background.jpg'),(700,500))

# mixer.init()
# mixer.music.load('jungles.ogg')
# mixer.music.play()

clock = time.Clock()


game = True 
while game:

    window.blit(background,(0,0))
    player.move()
    player.update()
    enemy.move()
    enemy.update()
    treasure.update()
    wall_1.update()


    for e in event.get():
        if e.type == QUIT: 
            game = False


    clock.tick(60)
    display.update()


