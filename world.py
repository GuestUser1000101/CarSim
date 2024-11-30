import pygame as pg
import sys
from car import *

class World:
    def __init__(self):
        self.car = Car(self, 2, 4, 1000, 10000)
        self.ground = 0
        self.gravity = 9.81
        self.pixels_per_meter = 3

    def update_world_physics(self, delta_time, inputs):
        for i in range(4):
            self.car.inputs[i] = inputs[i]
        self.car.update_physics(delta_time)

    def update_world_graphics(self, screen):
        screen.fill((0, 0, 0))
        self.car.draw(screen)
        self.car.draw_steering(screen, 450, 450)