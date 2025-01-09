from rendering_functions import *

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

def render_road(screen, road, pixels_per_meter):
    draw_loop(screen, (100, 100, 100), road, 10, pixels_per_meter)
