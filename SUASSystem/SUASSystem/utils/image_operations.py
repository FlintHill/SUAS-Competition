import math, exifread
from datetime import datetime
from SUASSystem import GCSSettings, inverse_haversine

def get_image_timestamp_from_filename(filename):
    filename = filename[6:]
    return float(filename[:-4])

def get_image_timestamp_from_metadata(path_to_image):
    image = open(path_to_image, "rb")
    tags = exifread.process_file(image, details=False)
    image_raw_time = tags["Image DateTime"]
    image_date_time = datetime.strptime(str(image_raw_time), "%Y:%m:%d %H:%M:%S")
    image_epoch_time = (image_date_time-datetime(1970,1,1)).total_seconds()
    return image_epoch_time


def get_target_gps_location(image_midpoint, target_midpoint, drone_gps_location):
    difference_x = target_midpoint[0] - image_midpoint[0]
    difference_y = target_midpoint[1] - image_midpoint[1]

    difference_x = (difference_x / math.sqrt(GCSSettings.IMAGE_PROC_PPSI)) / 12 #convert to feet
    difference_y = (difference_y / math.sqrt(GCSSettings.IMAGE_PROC_PPSI)) / 12 #convert to feet

    difference_point = (difference_x, difference_y, 0)
    return inverse_haversine(drone_gps_location, difference_point)
