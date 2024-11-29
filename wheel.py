import numpy as np
from physics_functions import *
import math


class Wheel:
    def __init__(self, car, mass, spring_strength, damping_strength, traction_function = None, drive_function = None):
        self.car = car

        # Basic Kinematics
        self.position = np.array((0, 0, 0))
        self.velocity = np.array((0, 0, 0))
        self.heading = 0
        self.mass = mass

        # Suspension
        self.spring_strength = spring_strength
        self.damping_strength = damping_strength

        # Traction
        self.traction_function = self.defaultTractionFunction if traction_function == None else traction_function

        # Drive
        self.power = 0
        self.drive_function = self.defaultDrivingFunction if drive_function == None else drive_function
    
    def get_dampening_force(self, delta_time):
        vertical_force =  -self.position * self.spring_strength - get_y(self.velocity) * self.damping_strength
        return np.array(0, 0, vertical_force)
    
    def get_steering_force(self, delta_time):
        steering_direction = np.array(math.cos(self.heading), math.sin(self.heading))
        steering_velocity = np.dot(self.car.velocity + self.velocity, steering_direction)
        
        if steering_velocity == 0:
            return np.empty()
        
        traction = self.traction_function(steering_velocity / np.linalg.norm(self.car.velocity + self.velocity))
        return -steering_velocity * traction / delta_time * steering_direction
        
    def get_driving_force(self, deltaTime):
        if self.power == 0:
            return np.empty()

        driving_direction = np.array(math.cos(self.heading + math.pi / 2), math.sin(self.heading + math.pi / 2))
        driving_velocity_percent = clamp(abs(np.dot(self.car.velocity, driving_direction) / self.car.max_speed), 0, 1)
        return driving_direction * self.drive_function(driving_velocity_percent) * self.power

    def defaultTractionFunction(percent_steering_velocity):
        if percent_steering_velocity < 0 or percent_steering_velocity > 1:
            raise Exception("Argument must be between 0 and 1")
        return -0.5 * math.floor(2 * percent_steering_velocity) + 0.6

    def defaultDrivingFunction(percent_driving_velocity):
        if percent_driving_velocity < 0 or percent_driving_velocity > 1:
            raise Exception("Argument must be between 0 and 1")
        return 4 * math.cos(math.pow(percent_driving_velocity, 1.5) - 0.4) - 3