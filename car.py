import numpy as np
import math
from physics_functions import *


class Car:
    def __init__(self, width, height, drivePower):
        self.velocity = np.array((0, 0, 0))
        self.position = np.array((0, 0, 0))
        self.rotation = 0
        self.rotational_velocity = 0
        self.max_speed = 50
        self.width = 2
        self.height = 4
        self.mass = 1000
        self.rotational_inertia = 2 / 5 * self.mass * math.pow((self.width + self.height) / 2, 2)

    def applyForceAtPosition(self, force, position):
        self.applyForce(force)
        torque = np.linalg.norm(force) * np.linalg.norm(position) * math.sin(get_signed_angle_between(force, -position))
        self.rotational_velocity += torque / self.rotational_inertia

    def applyForce(self, force):
        self.velocity += force / self.mass