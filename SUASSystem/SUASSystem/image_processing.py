from time import sleep
from PIL import Image
import os
import math
import random
from .utils import *
from UpdatedImageProcessing import *
from .settings import GCSSettings
from .converter_functions import inverse_haversine, get_mission_json
from .location import Location
"""
This file contains our image processing logic and utilizes our cropper function. 
"""
def run_img_proc_process(logger_queue, location_log, targets_to_submit, interop_client_array):
    while True:
        if len(targets_to_submit) > 0:
            target_characteristics = targets_to_submit.pop(0)

            target_time = get_image_timestamp_from_metadata("static/imgs/" + target_characteristics["base_image_filename"])

            closest_time_index = 0
            least_time_difference = location_log[0]["epoch_time"]
            for index in range(len(location_log)):
                difference_in_times = target_time - location_log[index]["epoch_time"]
                if abs(difference_in_times) <= least_time_difference:
                    closest_time_index = index
                    least_time_difference = difference_in_times
            drone_gps_location = Location(location_log[closest_time_index]["latitude"], location_log[closest_time_index]["longitude"], location_log[closest_time_index]["altitude"])

            image = Image.open("static/imgs/" + target_characteristics["base_image_filename"])
            image_midpoint = (image.width / 2, image.height / 2)
            target_midpoint = ((target_characteristics["target_top_left"][0] + target_characteristics["target_bottom_right"][0]) / 2, (target_characteristics["target_top_left"][1] + target_characteristics["target_bottom_right"][1]) / 2)
            target_location = get_target_gps_location(image_midpoint, target_midpoint, drone_gps_location)
            target_characteristics["latitude"] = target_location.get_lat()
            target_characteristics["longitude"] = target_location.get_lon()

            original_image_path = "static/all_imgs/" + target_characteristics["base_image_filename"]
            cropped_target_path = "static/crops/" + str(len(os.listdir('static/crops'))) + ".jpg"
            cropped_target_data_path = "static/crops/" + str(len(os.listdir('static/crops'))) + ".json"
            crop_target(original_image_path, cropped_target_path, target_characteristics["target_top_left"], target_characteristics["target_bottom_right"])
            save_json_data(cropped_target_data_path, target_characteristics)

            # comment out these lines if testing w/o interop
            if target_characteristics["type"] == "standard":
                interop_client_array[0].post_manual_standard_target(target_characteristics, cropped_target_path)
            elif target_characteristics["type"] == "emergent":
                interop_client_array[0].post_manual_emergent_target(target_characteristics, cropped_target_path)

        sleep(0.1)

def run_autonomous_img_proc_process(logger_queue, interop_client_array, img_proc_status, autonomous_targets_to_submit):
    while True:
        if len(autonomous_targets_to_submit) > 0:
            target_info = autonomous_targets_to_submit.pop()
            interop_client_array[0].post_autonomous_target(target_info)

        sleep(0.5)
