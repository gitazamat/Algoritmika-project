import pygame
import math
from pygame.locals import *

pygame.init()

window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('2д танчики')

background = pygame.transform.scale(pygame.image.load('background.png'), (window_width, window_height))

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_img, x, y, width, height, speed, route=None):
        super().__init__()
        self.original_image = pygame.transform.scale(pygame.image.load(sprite_img), (width, height))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.angle = 0
        self.route = route if route else []
        self.current_point_index = 0

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

    def move_along_route(self):
        if self.route:
            target_point = self.route[self.current_point_index]
            dx = target_point[0] - self.rect.centerx
            dy = target_point[1] - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist > self.speed:
                dx = dx / dist * self.speed
                dy = dy / dist * self.speed
                self.rect.x += dx
                self.rect.y += dy
            else:
                self.current_point_index = (self.current_point_index + 1) % len(self.route)

    def update(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.move_along_route()

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

player = GameSprite(sprite_img='player.png', x=100, y=300, width=50, height=50, speed=3)

# Define routes for each enemy tank
enemy_route1 = [(650, 450), (650, 350), (500, 350), (500, 450)]  # Bottom-right corner
enemy_route2 = [(650 , 270), (650, 130), (500, 130), (500, 270)]  # Top periphery
enemy_route3 = [(650, 300), (700, 300)]  # Closer to goal, middle horizontal line

enemy1 = GameSprite(sprite_img='enemy.png', x=650, y=400, width=50, height=50, speed=2, route=enemy_route1)
enemy2 = GameSprite(sprite_img='enemy.png', x=650, y=150, width=50, height=50, speed=2, route=enemy_route2)
enemy3 = GameSprite(sprite_img='enemy.png', x=650, y=300, width=50, height=50, speed=2, route=enemy_route3)

enemies = pygame.sprite.Group()
enemies.add(enemy1, enemy2, enemy3)

goal = GameSprite('goal.png', 700, 300, 70, 70, 0)

barriers = pygame.sprite.Group()
barrier1 = Barrier(200, 300, 100, 20)
barrier2 = Barrier(400, 200, 20, 150)
barriers.add(barrier1, barrier2)

bullets = pygame.sprite.Group()
pygame.font.init()
font1 = pygame.font.Font(None, 35)
clock = pygame.time.Clock()
running = True
respawn_timer = None
game_over = False
win_message = None

while running:
    current_time = pygame.time.get_ticks()

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

    if game_over:
        window.blit(win_message, (window_width // 2 - win_message.get_width() // 2, window_height // 2 - win_message.get_height() // 2))
        pygame.display.flip()
        continue

    if player.rect.colliderect(goal.rect):
        win_message = font1.render('Вы выиграли', True, (0, 255, 0))
        game_over = True

    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            win_message = font1.render('Вы проиграли', True, (255, 0, 0))
            game_over = True

    if respawn_timer and current_time >= respawn_timer:
        player.rect.center = (100, 300)
        respawn_timer = None

    player.move()
    player.update()
    goal.update()
    window.blit(goal.image, goal.rect)
    for barrier in barriers:
        if player.rect.colliderect(barrier.rect):
            player.rect.clamp_ip(window.get_rect())

    for enemy in enemies:
        enemy.update()

    bullets.update()
    for bullet in bullets:
        window.blit(bullet.image, bullet.rect)
        hit_enemies = pygame.sprite.spritecollide(bullet, enemies, True)
        if hit_enemies:
            bullets.remove(bullet)

    for barrier in barriers:
        pygame.draw.rect(window, (0, 0, 0, 0), barrier.rect)

    window.blit(player.image, player.rect)
    for enemy in enemies:
        window.blit(enemy.image, enemy.rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
