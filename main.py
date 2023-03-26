import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("CodeCool Tower")

WIDTH, HEIGHT = 1000, 800
FPS = 50
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))

def get_background(name):
    image = pygame.image.load(join("images", name))
    _, _, width, height = image.get_rect()
    tiles = list()
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = [i * width, j * height]
            tiles.append(pos)
    return tiles, image

def draw(window, background, bg_image, player, objects):
    for tile in background:
        window.blit(bg_image, tile)
    for obj in objects:
        obj.draw(window)

    player.draw(window)
    
    pygame.display.update()

def load_sprite_sheets(dir, width, height):
    path = join("images", dir)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = dict()

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = list()
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            #sprites.append(pygame.transform.scale2x(surface))
            sprites.append(surface)

            all_sprites[image.replace(".png", "")] = sprites
    return all_sprites

def get_block(size):
    path = join("images", "wall-tile.jpg")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return surface

class Player(pygame.sprite.Sprite):
    SPRITES = load_sprite_sheets("character", 64, 64)
    ANIMATION_DELAY = 10

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "right"
        self.animation_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    
    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def move_up(self, vel):
        self.y_vel = -vel
        if self.direction != "up":
            self.direction = "up"
            self.animation_count = 0

    def move_down(self, vel):
        self.y_vel = vel
        if self.direction != "down":
            self.direction = "down"
            self.animation_count = 0

    def loop(self, fps):
        self.move(self.x_vel, self.y_vel)
        self.update_sprite()
    
    def landed(self):
        self.count = 0
        self.y_vel *= 1
        self.rect.y = 650

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1
        self.rect.y = 90

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.x_vel != 0 or self.y_vel != 0:
            sprite_sheet = "move"

        sprite_sheet_name = sprite_sheet + "-" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win):
        win.blit(self.sprite, (self.rect.x, self.rect.y))

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name = None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

def handle_vertical_collision(player, objects, dy):
    collided_objects = list()
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

        collided_objects.append(obj)
    return collided_objects

def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    player.y_vel = 0
    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL)
    if keys[pygame.K_UP]:
        player.move_up(PLAYER_VEL)
    if keys[pygame.K_DOWN]:
        player.move_down(PLAYER_VEL)

    handle_vertical_collision(player, objects, player.y_vel)

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("stone-floor-tile.jpg")

    block_size = 50

    player = Player(100, 100, 50, 50)
    south_wall = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    north_wall = [Block(i * block_size, 0, block_size) for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    objects = [*south_wall, *north_wall]
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        player.loop(FPS)
        handle_move(player, objects)
        draw(window, background, bg_image, player, objects)
    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)