import pygame as pg
import sys


pg.__init__()
FPS = 60
clock = pg.time.Clock()

def physics(delta_time):
    pass

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    pg.display.update()
    delta_time = clock.tick(FPS) >> 10

    physics(delta_time)