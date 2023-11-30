import pygame
import math
import random
import time
from tkinter import *
from tkinter import messagebox


FPS = 60

WIDTH = 1540
HEIGHT = 900
chunk_size = 1
#tile_size соответсвует разрешению изображения
tile_size = 150
cam_speed = 15

WHITE = 0xFFFFFF

cam_x, cam_y = 0, 0
res = [1536, 960]
print(pygame.RESIZABLE)

pygame.init()
mouse_x, mouse_y = pygame.mouse.get_pos()
textures = {0:[pygame.image.load('0.png')],
             1:[pygame.image.load('1.png')]}

world_size_chunk_x = 25//chunk_size
world_size_chunk_y = 25//chunk_size


#Функция нормас работает
#chunck_on_screen() по положению камеры определяет, какие чанки из имеющихся нужно прорисовать на экране
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

#Функция по координате чанка определяет какая у него текстура(сейчас нет функционала)
def generate_tile(x, y, chunk_x, chunk_y):
    tile_x = (chunk_x//tile_size) + x
    tile_y = (chunk_y//tile_size) + y
    return int((chunk_x//chunk_size//tile_size)%2 == 0)


#Класс чанка
class Chunk():
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.map = [generate_tile(-1, y, self.x, self.y) for y in range(chunk_size) for x in range(chunk_size)]

    #render() прорисовывает нужный нам чанк, выцеживая, какая у него текстура(не прописано)
    def render(self, texture_code):
        for y in range(chunk_size):
            for x in range(chunk_size):
                texture = textures[texture_code][0]
                screen.blit(texture, (self.x + x*tile_size - cam_x, self.y + y*tile_size - cam_y))


#Чтение файла с кодами текстур чанков из памяти
chuncks_file = open('chuncks.txt','r+')
chuncks_texture_codes=[]
for i in range(625):
    just_code = chuncks_file.readline()
    chuncks_texture_codes.append(int(just_code))
chuncks_file.close()







c=0
window = pygame.display.set_mode((0,0), pygame.RESIZABLE)
fullscreen = pygame.display.set_mode((0,0), pygame.RESIZABLE)
screen = pygame.transform.scale(window,res)
finished = False
clock = pygame.time.Clock()
chunks = []
#создаём все чанки(пока нет работы с памятью)
for y in range(world_size_chunk_y):
    for x in range(world_size_chunk_x):
        chunks.append(Chunk(x*chunk_size*tile_size, y*chunk_size*tile_size))
while not finished:
    clock.tick(FPS)
    screen.fill(WHITE)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    print(clock.get_fps())

    #обработка зажатых клавиш
    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        if cam_x >= 15:
            cam_x -= cam_speed
    if key[pygame.K_w]:
        if cam_y >= 15:
            cam_y -= cam_speed
    if key[pygame.K_d]:
        if cam_x <= world_size_chunk_x * tile_size - res[0] - cam_speed:
            cam_x += cam_speed
    if key[pygame.K_s]:
        if cam_y <= world_size_chunk_y * tile_size - res[1] - cam_speed:
            cam_y += cam_speed

    #рендерим чанки, которые отображаются на экране
    for i in chunks_on_screen():
        chunks[i].render(chuncks_texture_codes[i])
    window.blit(pygame.transform.scale(screen, res), (0, 0))
    pygame.display.update()

    #обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            chuncks_file.close()
            finished = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                #делаем сохранение

                chuncks_file.close()
                chuncks_file = open('chuncks.txt','w')
                chuncks_file.seek(0)
                for i in range(625):
                    chuncks_file.write(str(chuncks_texture_codes[i])+'\n')
                chuncks_file.close()

                #закрываем программу
                finished = True

pygame.quit()