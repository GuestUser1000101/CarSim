import numpy as np


def get_x(vector):
    return vector[0]

def get_y(vector):
    return vector[1]

def get_z(vector):
    return vector[2]

def deadband(value, threshold, default = 0):
    return default if abs(value - default) < threshold else value

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))