#from SUASSystem import GCSSetting, inverse_haversine, get_mission_json
#from SUASSystem import GCSSetting
from SUASSystem.settings import GCSSettings
from SUASSystem.converter_functions import inverse_haversine, get_mission_json
import matplotlib.path
import numpy
import math

def get_target_gps_location(image_midpoint, target_midpoint, drone_gps_location):
    difference_x = target_midpoint[0] - image_midpoint[0]
    difference_y = target_midpoint[1] - image_midpoint[1]

    difference_x = (difference_x / math.sqrt(GCSSettings.IMAGE_PROC_PPSI)) / 12 #convert to feet
    difference_y = (difference_y / math.sqrt(GCSSettings.IMAGE_PROC_PPSI)) / 12 #convert to feet

    difference_point = (difference_x, difference_y, 0)
    return inverse_haversine(drone_gps_location, difference_point)

def construct_fly_zone_polygon(interop_client_array):
    mission_information_data = (get_mission_json(interop_client_array[0].get_active_mission(), interop_client_array[0].get_obstacles()))
    boundary_points = mission_information_data["search_grid_points"]
    point_list = []

    num_points = len(boundary_points)

    least_order = boundary_points[0]["order"]
    for i in range(len(boundary_points)):
        if boundary_points[i]["order"] < least_order:
            least_order = boundary_points[i]["order"]
    order = least_order
    count = 0
    while num_points > 0:
        if(count == len(boundary_points)):
            count = 0
        if(boundary_points[count]["order"] == order):
            point_list.append([boundary_points[count]["latitude"], boundary_points[count]["longitude"]])
            order+=1
            num_points-=1
        count+=1

    vertices = numpy.array(point_list)

    return matplotlib.path.Path(vertices)

def construct_fly_zone_polygon_from_json(interop_json):
    boundary_points = interop_json["search_grid_points"]
    point_list = []
    num_points = len(boundary_points)

    least_order = boundary_points[0]["order"]
    for i in range(len(boundary_points)):
        if boundary_points[i]["order"] < least_order:
            least_order = boundary_points[i]["order"]
    order = least_order
    count = 0
    while num_points > 0:
        if(count == len(boundary_points)):
            count = 0
        if(boundary_points[count]["order"] == order):
            point_list.append([boundary_points[count]["latitude"], boundary_points[count]["longitude"]])
            order+=1
            num_points-=1
        count+=1

    vertices = numpy.array(point_list)

    return matplotlib.path.Path(vertices)

def construct_runway_fly_zone():
    runway_zone = matplotlib.path.Path(numpy.array(GCSSettings.RUNWAY_POINTS))
    grass1_zone = matplotlib.path.Path(numpy.array(GCSSettings.GRASS1_POINTS))
    grass2_zone = matplotlib.path.Path(numpy.array(GCSSettings.GRASS2_POINTS))
    grass3_zone = matplotlib.path.Path(numpy.array(GCSSettings.GRASS3_POINTS))
    grass4_zone = matplotlib.path.Path(numpy.array(GCSSettings.GRASS4_POINTS))
    grass5_zone = matplotlib.path.Path(numpy.array(GCSSettings.GRASS5_POINTS))
    return runway_zone, grass1_zone, grass2_zone, grass3_zone, grass4_zone, grass5_zone
