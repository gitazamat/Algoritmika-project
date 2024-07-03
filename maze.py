from pygame import *
import pygame.sprite

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__()
        self.image = transform.scale(image.load(img), (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self, walls):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= 5
        if keys[K_s] and self.rect.y < 440:
            self.rect.y += 5
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= 5
        if keys[K_d] and self.rect.x < 640:
            self.rect.x += 5

        # Check for collisions with walls
        if pygame.sprite.spritecollide(self, walls, False):
            # Reset the player's position to prevent moving through walls
            self.rect.x = self.old_x
            self.rect.y = self.old_y

        # Update old position
        self.old_x = self.rect.x
        self.old_y = self.rect.y

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
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = Surface((w, h))
        self.image.fill((87, 239, 67))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Initialize game window and sprites
wall_1 = Wall(20, 20, 20, 500)
wall_2 = Wall(20, 20, 500, 20)
wall_3 = Wall(100, 100, 400, 20)
player = Player('hero.png', 300, 300)
enemy = Enemy('cyborg.png', 350, 200)
treasure = GameSprite('treasure.png', 600, 400)

# Create sprite groups
walls = pygame.sprite.Group(wall_1, wall_2, wall_3)
all_sprites = pygame.sprite.Group(player, enemy, treasure, wall_1, wall_2, wall_3)

# Initialize Pygame
pygame.init()
window = display.set_mode((700, 500))
display.set_caption('Maze Game')
background = transform.scale(image.load('background.jpg'), (700, 500))

clock = time.Clock()
game = True

while game:
    window.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            game = False

    player.move(walls)  # Pass walls to the move method of player
    enemy.move()
    
    all_sprites.update()  # Update all sprites
    all_sprites.draw(window)  # Draw all sprites on the window

    display.update()
    clock.tick(60)

pygame.quit()
