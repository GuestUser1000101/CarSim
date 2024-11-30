import pygame as pg
from pygame.locals import *
import sys
from world import *
from car import *
from wheel import *

pg.init()
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

    pg.display.update()
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
    world.update_world_graphics(DISPLAY)
    print(world.car.velocity)