# импортируем пайгейм
import pygame
import math
from pygame.locals import *

pygame.init()
# параметры окна
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('2д танчики')

background = pygame.transform.scale(pygame.image.load('background.png'), (window_width, window_height))
# класс gamesprite и другие
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_img, x, y, width, height, speed):
        super().__init__()
        self.original_image = pygame.transform.scale(pygame.image.load(sprite_img), (width, height))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.angle = 0

    def fire(self):
        bullet_speed = 15
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.angle, bullet_speed)
        bullets.add(bullet)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.bottom < window_height:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.right < window_width:
            self.rect.x += self.speed

    def rotate(self, angle_change):
        self.angle += angle_change
        if self.angle >= 360:
            self.angle -= 360
        if self.angle < 0:
            self.angle += 360

    def update(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def follow_player(self, player):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx /= dist
            dy /= dist
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, speed):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.speed = speed

    def update(self):
        self.rect.x += math.cos(math.radians(self.angle)) * self.speed
        self.rect.y -= math.sin(math.radians(self.angle)) * self.speed

class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))

def respawn_enemy(enemy_class, x, y, width, height, speed, delay):
    pygame.time.set_timer(pygame.USEREVENT + 1, delay)
    return GameSprite(sprite_img=enemy_class, x=x, y=y, width=width, height=height, speed=speed)
# отображение игроков и врагов
player = GameSprite(sprite_img='player.png', x=350, y=300, width=50, height=50, speed=10)

enemies = pygame.sprite.Group()
enemy1 = GameSprite(sprite_img='player1.png', x=340, y=280, width=45, height=45, speed=1)
enemy2 = GameSprite(sprite_img='player2.png', x=330, y=290, width=45, height=45, speed=2)
enemy3 = GameSprite(sprite_img='player3.png', x=320, y=220, width=45, height=45, speed=3)
enemies.add(enemy1, enemy2, enemy3)
# отображение бареров 
barriers = pygame.sprite.Group()
barrier1 = Barrier(200, 300, 100, 20)
barrier2 = Barrier(400, 200, 20, 150)
barriers.add(barrier1, barrier2)
# отображение пули
bullets = pygame.sprite.Group()

clock = pygame.time.Clock()
running = True
end = 0
# основной цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player.rotate(45)
            if event.key == pygame.K_SPACE: 
                player.fire()
        elif event.type == pygame.USEREVENT + 1:
            enemy1 = respawn_enemy('player1.png', 340, 280, 45, 45, 1, 0)
            enemy2 = respawn_enemy('player2.png', 330, 290, 45, 45, 2, 0)
            enemy3 = respawn_enemy('player3.png', 320, 220, 45, 45, 3, 0)
            enemies.add(enemy1, enemy2, enemy3)

    window.blit(background, (0, 0))

    player.move()
    player.update()

    for barrier in barriers:
        if player.rect.colliderect(barrier.rect):
            player.rect.clamp_ip(window.get_rect())

    for enemy in enemies:
        enemy.follow_player(player)
        enemy.move()
        enemy.update()

    bullets.update()
    for bullet in bullets:
        window.blit(bullet.image, bullet.rect)
        hit_enemies = pygame.sprite.spritecollide(bullet, enemies, True)
        if hit_enemies:
            bullets.remove(bullet)
            for hit_enemy in hit_enemies:
                enemies.remove(hit_enemy)
                pygame.time.set_timer(pygame.USEREVENT + 1, 3000)

    for barrier in barriers:
        pygame.draw.rect(window, (0, 0, 0, 0), barrier.rect)

    window.blit(player.image, player.rect)
    for enemy in enemies:
        window.blit(enemy.image, enemy.rect)

    end += 20
    if end > 100000000:
        print("Азамат победил😎")
        event.type = False
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
