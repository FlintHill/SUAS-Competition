from SUASSystem import GCSSettings, inverse_haversine, get_mission_json
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
    #mission_information_data["search_grid_points"]
    boundary_points = mission_information_data["fly_zones"][0]["boundary_pts"]
    point_list = []

    num_points = len(boundary_points)
    order = 1
    count = 0
    while num_points > 0:
        if(count = len(boundary_points)):
            count = 0
        if(boundary_points[count]["order"] == order):
            point_list.append([boundary_points[count]["latitude"], boundary_points[count]["longitude"]])
            order+=1
            num_points-=1
        count+=1

    vertices = numpy.array(point_list)

    return matplotlib.path.Path(vertices)
