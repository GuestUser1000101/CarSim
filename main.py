import pygame as pg
from pygame.locals import *
import sys
from world import *
from car import *
from wheel import *
import torch

pg.init()
pg.font.init()
font = pg.font.SysFont('Comic Sans MS', 10)
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500
DISPLAY = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

FPS = 60
clock = pg.time.Clock()
world = World()

while True:
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_TAB:
                world.debug = not world.debug
            if event.key == pg.K_r:
                world.reset()

    delta_time = clock.tick(FPS) / 1000
    

    world.update_world_physics(
        delta_time,
        (
            keys[pg.K_UP] or keys[pg.K_w],
            keys[pg.K_LEFT] or keys[pg.K_a],
            keys[pg.K_RIGHT] or keys[pg.K_d],
            keys[pg.K_DOWN] or keys[pg.K_s]
        )
    )
    world.update_world_graphics(DISPLAY, font)

    pg.display.update()