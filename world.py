import pygame as pg
import sys
from car import *
from road import *
from physics_functions import *

class World:
    def __init__(self):
        # Physics
        self.ground = 0 # Unused
        self.gravity = 9.81 #Unused

        # Rendering
        self.pixels_per_meter = 3
        self.debug = False

        # Road
        self.road = load_road_from_file('paths\\racetrack.txt')

        # The car
        self.car = Car(self, 2, 4, 1000, 3000)

    def update_world_physics(self, delta_time, inputs):
        reward = 0

        for i in range(4):
            self.car.inputs[i] = inputs[i]
        self.car.update_physics(delta_time)
        self.car.distance_to_next_segment = get_distance(self.car.position.tolist()[:2], self.road[(self.car.current_segment + 1) % len(self.road)])
        self.car.angle_to_next_segment = get_bound_angle(
            -get_angle_of_line(self.car.position, self.road[(self.car.current_segment + 1) % len(self.road)]) + math.pi / 2
            - self.car.rotation
        )
        if self.car.distance_to_next_segment < 5:
            self.car.current_segment = (self.car.current_segment + 1) % len(self.road)
            self.car.cumulative_segment += 1
            self.car.idle_time = 0
            reward = 10
        
        self.car.distance_to_road = distance_to_road(self.car.position, self.road, self.car.current_segment)
        self.car.is_on_road = self.car.distance_to_road < 5

        if not self.car.is_on_road or self.car.idle_time > 30:
            reward = -10
            return reward, True, self.car.current_segment

        return reward, False, self.car.current_segment

    def update_world_graphics(self, screen, font):
        screen.fill((0, 0, 0))
        render_road(screen, self.road, self.car.current_segment, self.pixels_per_meter)
        self.car.draw(screen)
        self.car.draw_steering(screen, 450, 450)
        
        if self.debug:
            draw_text(screen, font, (0, 255, 0) if self.car.is_on_road else (255, 0, 0), (10, 480), str(self.car.distance_to_road))

    def reset(self):
        self.car.reset()