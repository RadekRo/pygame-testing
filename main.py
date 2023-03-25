import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("CodeCool Tower")

WIDTH, HEIGHT = 1000, 800
FPS = 60
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

def draw(window, background, bg_image, player):
    for tile in background:
        window.blit(bg_image, tile)

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
        self.rect = self.sprite.get_rect(topLeft = (self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win):
        win.blit(self.sprite, (self.rect.x, self.rect.y))

def handle_move(player):
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

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("stone-floor-tile.jpg")

    player = Player(100, 100, 50, 50)

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        player.loop(FPS)
        handle_move(player)
        draw(window, background, bg_image, player)
    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)