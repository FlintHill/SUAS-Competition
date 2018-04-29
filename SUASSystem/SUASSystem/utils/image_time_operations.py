import math
import exifread
from datetime import datetime
import time

def get_image_timestamp_from_filename(filename):
    filename = filename[6:]
    return float(filename[:-4])

def get_image_timestamp_from_metadata(path_to_image):
    image = open(path_to_image, "rb")
    tags = exifread.process_file(image, details=False)
    image_raw_time = tags["Image DateTime"]
    image_date_time = int(datetime.strptime(str(image_raw_time), "%Y:%m:%d %H:%M:%S").strftime("%s"))
    image_epoch_time = image_date_time - time.time()

    return image_epoch_time
