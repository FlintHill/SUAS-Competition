from time import sleep
import os
import math
from utils import *
from .settings import GCSSettings
from .converter_functions import inverse_haversine
from ...UpdatedImageProcessing.ImageProcessing2.TargetDetection.single_target_map_detector import SingleTargetMapDetector
from PIL import Image

def run_img_proc_process(logger_queue, location_log, targets_to_submit, interop_client_array):
    while True:
        if len(targets_to_submit) > 0:
            target_characteristics = targets_to_submit.pop(0)

            if GCSSettings.UAV_VERSION == "10":
                target_time = utils.get_image_timestamp_from_filename(target_characteristics["base_image_filename"])
            elif GCSSettings.UAV_VERSION == "9.1":
                target_time = utils.get_image_timestamp_from_metadata("static/imgs/" + target_characteristics["base_image_filename"])
            else:
                raise Exception("Unknown drone type")

            closest_time_index = 0
            least_time_difference = location_log[0]["epoch_time"]
            for index in range(len(location_log)):
                difference_in_times = target_time - location_log[closest_time_index]["epoch_time"]
                if abs(difference_in_times) <= least_time_difference:
                    closest_time_index = index
                    least_time_difference = difference_in_times

            drone_gps_location = location_log[closest_time_index]["current_location"]
            image = Image.open("static/imgs/" + target_characteristics["base_image_filename"])
            image_midpoint = (image.width / 2, image.height / 2)
            target_midpoint = ((target_characteristics["target_top_left"][0] + target_characteristics["target_bottom_right"][0]) / 2, (target_characteristics["target_top_left"][1] + target_characteristics["target_bottom_right"][1]) / 2)
            target_location = utils.get_target_gps_location(image_midpoint, target_midpoint, drone_gps_location)
            target_characteristics["latitude"] = target_location.get_lat()
            target_characteristics["longitude"] = target_location.get_lon()

            original_image_path = "static/imgs/" + target_characteristics["base_image_filename"]
            cropped_target_path = "static/crops/" + str(len(os.listdir('static/crops'))) + ".jpg"
            cropped_target_data_path = "static/crops/" + str(len(os.listdir('static/crops'))) + ".json"
            utils.crop_target(original_image_path, cropped_target_path, target_characteristics["target_top_left"], target_characteristics["target_bottom_right"])
            utils.save_json_data(cropped_target_data_path, target_characteristics)

            interop_client_array[0].post_standard_target(target_characteristics, cropped_target_path)

        sleep(0.1)

def run_autonomous_img_proc_process(logger_queue, location_log, interop_client_array, img_proc_status):
    target_detected = []
    target_map_path = "static/imgs"
    autonomous_image_processing_save_path = "static/autonomous_crops"

    while True:
        amount_of_target_maps_present = len(set(os.listdir(target_map_path))) - len(set(target_detected))

        while (amount_of_target_maps_present > 0):
            if (img_proc_status.value == "connected"):
                current_target_map_name = ""

                for index_1 in range(len(set(os.listdir(target_map_path)))):
                    current_target_map_name = os.listdir(target_map_path)[index_1]

                    is_current_target_map_detected = False
                    for index_2 in range(len(target_detected)):
                        if (target_detected[index_2] == current_target_map_name):
                            is_current_target_map_detected = True

                    if (is_current_target_map_detected == False):
                        target_detected.append(current_target_map_name)
                        break

                combo_target_detection_result_list = SingleTargetMapDetector.detect_single_target_map(os.path.join(target_map_path, current_target_map_name))
                single_target_crops = combo_target_detection_result_list[0]
                json_file = combo_target_detection_result_list[1]

                '''
                if GCSSettings.UAV_VERSION == "10":
                    target_time = utils.get_image_timestamp_from_filename(target_characteristics["base_image_filename"])
                elif GCSSettings.UAV_VERSION == "9.1":
                    target_time = utils.get_image_timestamp_from_metadata("static/imgs/" + target_characteristics["base_image_filename"])
                else:
                    raise Exception("Unknown drone type")

                closest_time_index = 0
                least_time_difference = location_log[0]["epoch_time"]
                for index in range(len(location_log)):
                    difference_in_times = target_time - location_log[closest_time_index]["epoch_time"]
                    if abs(difference_in_times) <= least_time_difference:
                        closest_time_index = index
                        least_time_difference = difference_in_times

                drone_gps_location = location_log[closest_time_index]["current_location"]
                image = Image.open("static/imgs/" + target_characteristics["base_image_filename"])
                image_midpoint = (image.width / 2, image.height / 2)
                target_midpoint = ((target_characteristics["target_top_left"][0] + target_characteristics["target_bottom_right"][0]) / 2, (target_characteristics["target_top_left"][1] + target_characteristics["target_bottom_right"][1]) / 2)
                target_location = utils.get_target_gps_location(image_midpoint, target_midpoint, drone_gps_location)
                target_characteristics["latitude"] = target_location.get_lat()
                target_characteristics["longitude"] = target_location.get_lon()
                '''

                for index_3 in range(len(single_target_crops)):
                    single_target_crops[index_3].save(os.path.join(autonomous_image_processing_save_path, current_target_map_name + " - " + str(index_3 + 1) + ".png"))

                with open(os.path.join(autonomous_image_processing_save_path, current_target_map_name + ".json"), 'w') as fp:
                    json.dump(json_file, fp, indent=4)

                amount_of_target_maps_present -= 1

                '''
                original_image_path = "static/imgs/" + target_characteristics["base_image_filename"]
                cropped_target_path = "static/autonomous_crops/" + str(len(os.listdir('static/autonomous_crops'))) + ".jpg"
                cropped_target_data_path = "static/autonomous_crops/" + str(len(os.listdir('static/autonomous_crops'))) + ".json"
                #utils.crop_target(original_image_path, cropped_target_path, target_characteristics["target_top_left"], target_characteristics["target_bottom_right"])
                utils.save_json_data(cropped_target_data_path, target_characteristics)

                interop_client_array[0].post_standard_target(target_characteristics, cropped_target_path)
                '''
