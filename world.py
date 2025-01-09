import pygame as pg
import sys
from car import *
from road import *

class World:
    def __init__(self):
        # The car
        self.car = Car(self, 2, 4, 1000, 3000)

        # Physics
        self.ground = 0 # Unused
        self.gravity = 9.81 #Unused

        # Rendering
        self.pixels_per_meter = 3
        self.debug = True

        # Road
        self.road = load_road_from_file('paths\\circle.txt')

    def update_world_physics(self, delta_time, inputs):
        for i in range(4):
            self.car.inputs[i] = inputs[i]
        self.car.update_physics(delta_time)

    def update_world_graphics(self, screen):
        screen.fill((0, 0, 0))
        render_road(screen, self.road, self.pixels_per_meter)
        self.car.draw(screen)
        self.car.draw_steering(screen, 450, 450)
        