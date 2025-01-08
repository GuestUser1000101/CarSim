import numpy as np
from physics_functions import *
import math


class Wheel:
    def __init__(self, car, position, mass, spring_strength, damping_strength, traction_function = None, drive_function = None):
        self.car = car

        # Basic Kinematics
        self.position = position
        self.velocity = np.array((0.0, 0.0, 0.0))
        self.rotation = 0
        self.mass = mass

        # Suspension
        self.spring_strength = spring_strength
        self.damping_strength = damping_strength

        # Traction
        self.traction_function = self.default_traction_function if traction_function == None else traction_function
        self.wheel_friction = 100

        # Drive
        self.power = 0
        self.drive_function = self.default_driving_function if drive_function == None else drive_function
    
    # Unused
    def get_suspension_force(self, delta_time):
        vertical_force = (self.car.world.ground - (get_z(self.car.position) + get_z(self.position))) * self.spring_strength - abs(get_z(self.car.velocity)) * self.damping_strength
        return np.array([0, 0, vertical_force])
    
    def get_steering_force(self, delta_time):
        steering_direction = np.array([math.cos(self.rotation), math.sin(self.rotation), 0])
        global_velocity = (
            rotate_vector(
                self.car.rotational_velocity * self.position,
                -math.pi / 2
            ) +
            rotate_vector(self.car.velocity, -self.car.rotation) +
            self.velocity
        )
        
        steering_velocity = np.dot(global_velocity, steering_direction)
        
        if steering_velocity == 0:
            return np.empty(3)
        
        traction = self.traction_function(abs(steering_velocity / np.linalg.norm(global_velocity)))
        # removing wheel_friction - it is just traction
        # removing traction - unecessary complexity, add back later
        return -steering_velocity / delta_time * self.car.mass / 4 * steering_direction #* self.wheel_friction * traction 
        
    def get_driving_force(self, deltaTime):
        if self.power == 0:
            return np.empty(3)

        driving_direction = np.array([abs(math.cos(self.rotation + math.pi / 2)), abs(math.sin(self.rotation + math.pi / 2)), 0])
        
        driving_velocity_percent = clamp(abs(np.dot(rotate_vector(self.car.velocity, -self.car.rotation), driving_direction) / self.car.max_speed), 0, 1)
        return driving_direction * self.drive_function(driving_velocity_percent) * self.power

    def default_traction_function(self, percent_steering_velocity):
        if percent_steering_velocity < 0 or percent_steering_velocity > 1:
            raise Exception("Argument must be between 0 and 1")
        return -0.5 * math.floor(2 * percent_steering_velocity) + 0.6

    def default_driving_function(self, percent_driving_velocity):
        if percent_driving_velocity < 0 or percent_driving_velocity > 1:
            raise Exception("Argument must be between 0 and 1")
        return 4 * math.cos(math.pow(percent_driving_velocity, 1.5) - 0.4) - 3

    def apply_forces_to_car(self, delta_time):
        #net_force = self.get_suspension_force(delta_time) + self.get_driving_force(delta_time) + self.get_steering_force(delta_time)
        net_force = self.get_driving_force(delta_time) + self.get_steering_force(delta_time)
        self.car.apply_force_at_position(net_force, self.position, delta_time)

    def update_physics(self, delta_time):
        self.position += self.velocity * delta_time

    def is_on_ground(self):
        return get_z(self.position) + get_z(self.car.position) <= self.car.world.ground