import pygame
import math
from pygame.locals import *

pygame.init()

# Определение размеров окна и создание окна
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('2д танчики')

# Загрузка изображений
background = pygame.transform.scale(pygame.image.load('background.png'), (window_width, window_height))

# Класс для спрайтов игры
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
        # Этот метод пока не реализован, поэтому он пустой
        pass

    def move(self):
        # Движение игрока с учетом столкновений с барьерами и границами окна
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


class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))

# Создание игрока (танка)
player = GameSprite(sprite_img='player.png', x=350, y=300, width=50, height=50, speed=3)

# Создание врагов (танков)
player1 = GameSprite(sprite_img='player1.png', x=340, y=280, width=45, height=45, speed=1)
player2 = GameSprite(sprite_img='player2.png', x=330, y=290, width=45, height=45, speed=1)
player3 = GameSprite(sprite_img='player3.png', x=320, y=220, width=45, height=45, speed=1)

# Создание барьеров (невидимых прямоугольников)
barriers = pygame.sprite.Group()
barrier1 = Barrier(200, 300, 100, 20)
barrier2 = Barrier(400, 200, 20, 150)
barriers.add(barrier1, barrier2)

# Основной игровой цикл
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player.rotate(45)

    window.blit(background, (0, 0))  # Отрисовка фона

    player.move()  # Движение игрока
    player.update()  # Обновление игрока (поворот)

    # Проверка столкновений с барьерами
    for barrier in barriers:
        if player.rect.colliderect(barrier.rect):
            player.rect.clamp_ip(window.get_rect())

    # Преследование игрока врагами
    player1.follow_player(player)
    player2.follow_player(player)
    player3.follow_player(player)

    player1.move()  # Движение врага
    player1.update()  # Обновление врага (поворот)
    player2.move()  # Движение врага
    player2.update()  # Обновление врага (поворот)
    player3.move()  # Движение врага
    player3.update()  # Обновление врага (поворот)

    # Отрисовка барьеров (прямоугольников)
    for barrier in barriers:
        pygame.draw.rect(window, (0, 0, 0, 0), barrier.rect)

    # Отрисовка игрока и врагов
    window.blit(player.image, player.rect)
    window.blit(player1.image, player1.rect)
    window.blit(player2.image, player2.rect)
    window.blit(player3.image, player3.rect)

    pygame.display.flip()  # Обновление экрана
    clock.tick(60)  # Ограничение частоты кадров

pygame.quit()
