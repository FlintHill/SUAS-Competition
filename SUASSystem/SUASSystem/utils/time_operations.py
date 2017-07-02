import exifread
from datetime import datetime

def get_image_timestamp(filename):
    opened_file = open(filename, 'rb')
    tags = exifread.process_file(opened_file)
    image_raw_time = tags['Image DateTime']
    converted_time = datetime.strptime(str(image_raw_time), "%Y:%m:%d %H:%M:%S")

    return converted_time
