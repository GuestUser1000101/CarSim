from rendering_functions import *
from physics_functions import *

def load_road_from_file(path):
    file = open(path, "r")
    road = []
    node = file.readline()
    while (len(node) != 0):
        road.append(tuple(map(float, node.split(", "))))
        node = file.readline()

    file.close()

    print("Path Loaded:")
    for waypoint in road:
        print(waypoint)
    
    return road

def render_road(screen, road, current_segment, pixels_per_meter):
    draw_loop(screen, (100, 100, 100), road, 10, current_segment, pixels_per_meter)

def distance_to_road(position, road, current_segment):
    import math

    def get_distance(point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    startpoint = road[current_segment]
    endpoint = road[(current_segment + 1) % len(road)]
    
    line_vec = (endpoint[0] - startpoint[0], endpoint[1] - startpoint[1])
    point_vec = (position[0] - startpoint[0], position[1] - startpoint[1])
    
    line_length_squared = line_vec[0]**2 + line_vec[1]**2
    t = max(0, min(1, (point_vec[0] * line_vec[0] + point_vec[1] * line_vec[1]) / line_length_squared))
    
    closest_point = (startpoint[0] + t * line_vec[0], startpoint[1] + t * line_vec[1])
    
    return get_distance(position, closest_point)