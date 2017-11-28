import math
from SUASSystem import GCSSettings, inverse_haversine

def get_image_timestamp(filename):
    filename = filename[5:]
    return float(filename[:-4])

def get_target_gps_location(image_midpoint, target_midpoint, drone_gps_location):
    difference_x = target_midpoint[0] - image_midpoint[0]
    difference_y = target_midpoint[1] - image_midpoint[1]

    difference_x = (difference_x / math.sqrt(GCSSettings.IMAGE_PROC_PPSI)) / 12 #convert to feet
    difference_y = (difference_y / math.sqrt(GCSSettings.IMAGE_PROC_PPSI)) / 12 #convert to feet

    difference_point = (difference_x, difference_y, 0)
    return = inverse_haversine(drone_gps_location, difference_point)
