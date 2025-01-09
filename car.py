import numpy as np
import math
from physics_functions import *
from rendering_functions import *
from wheel import *
import pygame as pg


class Car:
    def __init__(self, world, width, length, mass, drive_power, driving_wheels = (1, 1, 0, 0), steering_wheels = (1, 1, 0, 0)):
        # Kinematics
        self.position = np.array((0.0, 0.0, 0.0))
        self.velocity = np.array((0.0, 0.0, 0.0))
        self.max_speed = 50 # Unused
        self.rotation = 0
        self.rotational_velocity = 0

        # Environment
        self.world = world

        # Constants
        self.width = width
        self.length = length
        self.drive_power = drive_power
        self.mass = mass
        self.rotational_inertia = 2 / 5 * self.mass * math.pow((self.width + self.length) / 2, 2)

        # Wheels (front_left, front_right, back_left, back_right)
        self.driving_wheels = driving_wheels
        self.steering_wheels = steering_wheels
        self.wheels = [
            Wheel(self, np.array([-self.width / 2, self.length / 2, -0.5]), 100, 100, 10),
            Wheel(self, np.array([self.width / 2, self.length / 2, -0.5]), 100, 100, 10),
            Wheel(self, np.array([-self.width / 2, -self.length / 2, -0.5]), 100, 100, 10),
            Wheel(self, np.array([self.width / 2, -self.length / 2, -0.5]), 100, 100, 10)
        ]

        # Inputs (fowards, left, right, backward)
        self.inputs = [False, False, False, False]
        self.steering_angle = 0
        self.steering_angle_velocity = 0
        self.steering_angle_speed = 0.5
        self.steering_angle_dampen = 0.25

    def apply_force_at_position(self, force, position, delta_time):
        self.apply_force(force, delta_time)
        torque = np.linalg.norm(force) * np.linalg.norm(position) * math.sin(get_signed_angle_between(-position, force))
        self.rotational_velocity += torque / self.rotational_inertia * delta_time

    def apply_force(self, force, delta_time):
        self.velocity += rotate_vector(force / self.mass * delta_time, self.rotation)

    def update_physics(self, delta_time):
        #self.velocity += np.array([0, 0, -1]) * self.world.gravity * delta_time
        set_z(self.position, 0)

        forward_input, left_input, right_input, backward_input = [self.inputs[i] for i in range(4)]

        if left_input and right_input:
            self.steering_angle_velocity = 0
        elif left_input:
            self.steering_angle_velocity = self.steering_angle_speed * (2 if self.steering_angle < 0 else 1)
        elif right_input:
            self.steering_angle_velocity = -self.steering_angle_speed * (2 if self.steering_angle > 0 else 1)
        else:
            self.steering_angle_velocity = -self.steering_angle / delta_time * self.steering_angle_dampen

        self.steering_angle_velocity = get_deadband(self.steering_angle_velocity, 0.01)
        self.steering_angle += self.steering_angle_velocity * delta_time
        self.steering_angle = clamp(self.steering_angle, -math.pi / 4, math.pi / 4)
        self.steering_angle = get_deadband(self.steering_angle, 0.001)

        if self.steering_angle != 0:
            turn_radius = self.length / math.tan(self.steering_angle)

        for wheel, is_steering in zip(self.wheels, self.steering_wheels):
            wheel.update_physics(delta_time)
            if is_steering:
                if self.steering_angle != 0:
                    wheel.rotation = math.atan(self.length / (turn_radius - get_x(wheel.position)))
                else:
                    wheel.rotation = 0

        for wheel, is_driving in zip(self.wheels, self.driving_wheels):
            if is_driving:
                wheel.power = (int(forward_input) - int(backward_input)) * self.drive_power
            wheel.apply_forces_to_car(delta_time)
        
        self.rotation += self.rotational_velocity * delta_time
        self.position += self.velocity * delta_time
    
    def draw(self, screen):
        draw_rect(screen, (255, 0, 0), self.position, self.length, self.width, self.rotation, self.world.pixels_per_meter)
        if self.world.debug:
            draw_vector(screen, (0, 255, 0), self.position, self.velocity, 2, 0.1, self.world.pixels_per_meter)
        for wheel in self.wheels:
            draw_rect(screen, (0, 255, 255), self.position + rotate_vector(wheel.position, self.rotation), 1, 0.4, self.rotation + wheel.rotation, self.world.pixels_per_meter)
            if self.world.debug:
                draw_vector(screen, (255, 255, 0), self.position + rotate_vector(wheel.position, self.rotation), rotate_vector(wheel.steering_force, self.rotation), 1, 0.01, self.world.pixels_per_meter)
                draw_vector(screen, (255, 0, 255), self.position + rotate_vector(wheel.position, self.rotation), rotate_vector(wheel.driving_force, self.rotation), 1, 0.01, self.world.pixels_per_meter)
    
    def draw_steering(self, screen, screen_x, screen_y):
        draw_rect(screen, (255, 255, 255), np.array([screen_x, screen_y]), 60, 75, self.steering_angle)