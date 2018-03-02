from time import sleep
from PIL import Image
import os
import math
from .utils import *
from UpdatedImageProcessing.TargetDetection.single_target_map_detector import SingleTargetMapDetector
from .settings import GCSSettings
from .converter_functions import inverse_haversine

def run_img_proc_process(logger_queue, location_log, targets_to_submit, interop_client_array):
    while True:
        if len(targets_to_submit) > 0:
            target_characteristics = targets_to_submit.pop(0)

            if GCSSettings.UAV_VERSION == "10":
                target_time = get_image_timestamp_from_filename(target_characteristics["base_image_filename"])
            elif GCSSettings.UAV_VERSION == "9.1":
                target_time = get_image_timestamp_from_metadata("static/imgs/" + target_characteristics["base_image_filename"])
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
            target_location = get_target_gps_location(image_midpoint, target_midpoint, drone_gps_location)
            target_characteristics["latitude"] = target_location.get_lat()
            target_characteristics["longitude"] = target_location.get_lon()

            original_image_path = "static/imgs/" + target_characteristics["base_image_filename"]
            cropped_target_path = "static/crops/" + str(len(os.listdir('static/crops'))) + ".jpg"
            cropped_target_data_path = "static/crops/" + str(len(os.listdir('static/crops'))) + ".json"
            crop_target(original_image_path, cropped_target_path, target_characteristics["target_top_left"], target_characteristics["target_bottom_right"])
            save_json_data(cropped_target_data_path, target_characteristics)

            if target_characteristics["type"] == "standard":
                interop_client_array[0].post_manual_standard_target(target_characteristics, cropped_target_path)
            elif target_characteristics["type"] == "emergent":
                interop_client_array[0].post_manual_emergent_target(target_characteristics, cropped_target_path)

        sleep(0.1)

def run_autonomous_img_proc_process(logger_queue, location_log, interop_client_array, img_proc_status):
    target_detected = []
    TARGET_MAP_PATH = "static/imgs"
    AUTONOMOUS_IMAGE_PROCESSING_SAVE_PATH = "static/autonomous_crops"
    while True:
        amount_of_target_maps_present = len(set(os.listdir(TARGET_MAP_PATH))) - len(set(target_detected))

        while (amount_of_target_maps_present > 0):
            for index_in_target_map_path in range(len(set(os.listdir(TARGET_MAP_PATH)))):
                current_target_map_name = os.listdir(TARGET_MAP_PATH)[index_in_target_map_path]

                is_current_target_map_detected = False
                for index_in_target_detected in range(len(target_detected)):
                    if (target_detected[index_in_target_detected] == current_target_map_name):
                        is_current_target_map_detected = True

                if (is_current_target_map_detected == False):
                    target_detected.append(current_target_map_name)
                    break

            combo_target_detection_result_list = SingleTargetMapDetector.detect_single_target_map(os.path.join(TARGET_MAP_PATH, current_target_map_name))
            single_target_crops = combo_target_detection_result_list[0]
            json_file = combo_target_detection_result_list[1]

            image = Image.open(os.path.join(TARGET_MAP_PATH, current_target_map_name))
            json_file["target_map_center_location"] = (image.width / 2, image.height / 2)
            json_file["target_map_timestamp"] = utils.get_image_timestamp_from_metadata(os.path.join(TARGET_MAP_PATH, current_target_map_name))


            """
            drone_gps_location = location_log[closest_time_index]["current_location"]
            image = Image.open("static/imgs/" + target_characteristics["base_image_filename"])
            image_midpoint = (image.width / 2, image.height / 2)
            target_midpoint = ((target_characteristics["target_top_left"][0] + target_characteristics["target_bottom_right"][0]) / 2, (target_characteristics["target_top_left"][1] + target_characteristics["target_bottom_right"][1]) / 2)
            target_location = utils.get_target_gps_location(image_midpoint, target_midpoint, drone_gps_location)
            target_characteristics["latitude"] = target_location.get_lat()
            target_characteristics["longitude"] = target_location.get_lon()
            """

            for index_in_single_target_crops in range(len(single_target_crops)):
                json_file["image_processing_results"][index_in_single_target_crops]["target_index"] = index_in_single_target_crops + 1

                current_crop_path = os.path.join(AUTONOMOUS_IMAGE_PROCESSING_SAVE_PATH, current_target_map_name + " - " + str(index_in_single_target_crops + 1) + ".png")
                single_target_crops[index_in_single_target_crops].save(current_crop_path)

                shape_type = ShapeClassification(current_crop_path).get_shape_type()
                json_file["image_processing_results"][index_in_single_target_crops]["target_shape_type"] = shape_type

                color_classifying_results = ColorClassifier(current_crop_path).get_color()
                shape_color = color_classifying_results[0]
                letter_color = color_classifying_results[1]
                json_file["image_processing_results"][index_in_single_target_crops]["target_shape_color"] = shape_color
                json_file["image_processing_results"][index_in_single_target_crops]["target_letter_color"] = letter_color

                # adds target location
                target_map_center_pixel_coordinates = json_file["target_map_center_location"]
                target_pixel_coordinates = json_file["image_processing_results"][index_in_single_target_crops]["target_location"]
                target_time = json_file["target_map_timestamp"]

                closest_time_index = 0
                least_time_difference = location_log[0]["epoch_time"]
                for index in range(len(location_log)):
                    difference_in_times = target_time - location_log[closest_time_index]["epoch_time"]
                    if abs(difference_in_times) <= least_time_difference:
                        closest_time_index = index
                        least_time_difference = difference_in_times

                drone_gps_location = location_log[closest_time_index]["current_location"]

                target_location = utils.get_target_gps_location(target_map_center_pixel_coordinates, target_pixel_coordinates, drone_gps_location)
                json_file["image_processing_results"][index_in_single_target_crops]["latitude"] = target_location.get_lat()
                json_file["image_processing_results"][index_in_single_target_crops]["longitude"] = target_location.get_lon()

            with open(os.path.join(AUTONOMOUS_IMAGE_PROCESSING_SAVE_PATH, current_target_map_name + ".json"), 'w') as fp:
                json.dump(json_file, fp, indent=4)

            amount_of_target_maps_present -= 1
