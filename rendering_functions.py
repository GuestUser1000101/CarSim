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
        points.append(((get_x(position) + rel_x) * pixels_per_meter, (get_y(position) + rel_y) * pixels_per_meter))

    pg.draw.polygon(screen, color, points)

def draw_vector(screen, color, position, vector, weight = 1, vector_scale = 1, pixels_per_meter = 1):
    pg.draw.line(screen, color, (position * pixels_per_meter).tolist()[:2], ((position + vector * vector_scale) * pixels_per_meter).tolist()[:2], weight)

def draw_loop(screen, color, points, weight = 10, highlight_segment = -1, pixels_per_meter = 1):
    for i in range(len(points)):
        pg.draw.circle(
            screen,
            (180, 180, 40) if highlight_segment == i else color,
            tuple(map(lambda x : x * pixels_per_meter, points[(i + 1) % len(points)])),
            weight * pixels_per_meter / 2
        )

        pg.draw.line(
            screen,
            color if highlight_segment != i else (180, 180, 40),
            tuple(map(lambda x : x * pixels_per_meter, points[i])),
            tuple(map(lambda x : x * pixels_per_meter, points[(i + 1) % len(points)])),
            weight * pixels_per_meter
        )

def draw_text(screen, font, color, position, text):
    surface = font.render(text, False, color)
    screen.blit(surface, position)