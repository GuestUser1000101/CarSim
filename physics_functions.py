import numpy as np
import math


def get_x(vector):
    return vector[0]

def get_y(vector):
    return vector[1]

def get_z(vector):
    return vector[2]

def set_x(vector, value):
    vector[0] = value

def set_y(vector, value):
    vector[1] = value

def set_z(vector, value):
    vector[2] = value

def get_deadband(value, threshold, default = 0):
    return default if abs(value - default) < threshold else value

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

def get_angle_between(vector1, vector2):
    return math.acos(np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2)))

def get_signed_angle_between(vector1, vector2):
    theta = math.atan2(get_y(vector2), get_x(vector2)) - math.atan2(get_y(vector1), get_x(vector1))
    return theta - 2 * math.pi if theta > math.pi else theta

def get_unit(vector):
    return vector / np.linalg.norm(vector)