import numpy as np


class Car:
    def __init__(self):
        self.velocity = np.array((0, 0, 0))
        self.position = np.array((0, 0, 0))
        self.heading = 0
        self.max_speed = 10