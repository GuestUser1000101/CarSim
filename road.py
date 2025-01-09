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
    startpoint = road[current_segment]
    endpoint = road[(current_segment + 1) % len(road)]
    
    return (
        abs(
            (endpoint[0] - startpoint[0]) * (position[1] - startpoint[1])
            - (endpoint[1] - startpoint[1]) * (position[0] - startpoint[0])
        )
        / get_distance(startpoint, endpoint)
    )
