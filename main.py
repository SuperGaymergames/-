import pygame
import math
import random
import time
from tkinter import *
from tkinter import messagebox


FPS = 48

WIDTH = 1540
HEIGHT = 900
chunk_size = 26
tile_size = 8
world_size = [3, 2]

WHITE = 0xFFFFFF

cam_x, cam_y = 0, 0
res = [400, 400]
size = [800, 800]

pygame.init()
mouse_x, mouse_y = pygame.mouse.get_pos()
textures = {0:[pygame.image.load('0.png')],
             1:[pygame.image.load('1.png')]}

world_size_chunk_x = 384//chunk_size
world_size_chunk_y = 256//chunk_size



def chunks_on_screen():
    x1 = cam_x//(chunk_size*tile_size)
    y1 = cam_y//(chunk_size*tile_size)

    x2 = (cam_x + res[0]) //(chunk_size * tile_size)
    y2 = (cam_y + res[1]) //(chunk_size * tile_size)

    x1 = min(max(x1, 0), world_size_chunk_x - 1)
    x2 = min(max(x2, 0), world_size_chunk_x - 1)

    y1 = min(max(y1, 0), world_size_chunk_y - 1)
    y2 = min(max(y2, 0), world_size_chunk_y - 1)

    result = []
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            result.append(x+y*world_size_chunk_x)
    return result

def generate_tile(x, y, chunk_x, chunk_y):
    tile_x = (chunk_x//tile_size) + x
    tile_y = (chunk_y//tile_size) + y
    return int((chunk_x//chunk_size//tile_size)%2 == 0)

class Chunk():
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.map = [generate_tile(x, y, self.x, self.y) for y in range(chunk_size) for x in range(chunk_size)]
    def render(self):
        for y in range(chunk_size):
            for x in range(chunk_size):
                texture = textures[self.map[x + y * chunk_size]][0]
                screen.blit(texture, (self.x + x*tile_size - cam_x, self.y + y*tile_size - cam_y))









window = pygame.display.set_mode(size)
screen = pygame.transform.scale(window, res)
finished = False
clock = pygame.time.Clock()
chunks = []
for y in range(world_size_chunk_y):
    for x in range(world_size_chunk_x):
        chunks.append(Chunk(x*chunk_size*tile_size, y*chunk_size*tile_size))

while not finished:
    clock.tick(FPS)
    screen.fill(WHITE)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        if cam_x >= 15:
            cam_x -= 15
    if key[pygame.K_w]:
        if cam_y >= 15:
            cam_y -= 15
    if key[pygame.K_d]:
        if cam_x <= 384 * tile_size - 580:
            cam_x += 15
    if key[pygame.K_s]:
        if cam_y <= 256 * tile_size - 580:
            cam_y += 15

    for i in chunks_on_screen():
        chunks[i].render()
    window.blit(pygame.transform.scale(screen, size), (0, 0))
    print(cam_x)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                finished = True

pygame.quit()