import math
import pygame as pg
from physics_functions import *

def draw_rect(screen, color, position, length, width, rot, pixels_per_meter = 1):
    points = []
    radius = math.sqrt(math.pow(length / 2, 2) + math.pow(width / 2, 2))

    angle = math.atan2(length / 2, width / 2)
    angles = [angle, -angle + math.pi, angle + math.pi, -angle]

    for angle in angles:
        rel_y = -radius * math.sin(angle + rot)
        rel_x = radius * math.cos(angle + rot)
        points.append(((get_x(position) + rel_x) * pixels_per_meter, screen.get_size()[1] - (get_y(position) + rel_y) * pixels_per_meter))

    pg.draw.polygon(screen, color, points)