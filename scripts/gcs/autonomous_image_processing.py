from PIL import Image
import os
import random
from .flask_gcs import *
from ...SUASSystem.SUASSystem.utils import *
from UpdatedImageProcessing import *
from ...SUASSystem.SUASSystem.settings import GCSSettings

def initialize_autonomous_image_processing_process():
    clear_to_run = True

    location_log_json = get_uav_location_log()

    if location_log_json["request_status"] == "success":
        location_log = location_log_json["location_log"]:
    else:
        clear_to_run = False

    interop_client_array = get_interop_client_array()

    if interop_client_array_json["request_status"] == "success":
        interop_client_array = interop_client_array_json["interop_client"]:
    else:
        clear_to_run = False

    if clear_to_run:
        run_autonomous_img_proc_process(location_log, interop_client_array)

def run_autonomous_img_proc_process(location_log, interop_client_array):
    TARGET_MAP_PATH = "static/imgs/"
    AUTONOMOUS_IMAGE_PROCESSING_SAVE_PATH = "static/autonomous_crops"
    submitted_target_locations = []

    while True:
        current_target_map_name = receive_image_filenames.recv()
        current_target_map_path = os.path.join(TARGET_MAP_PATH, current_target_map_name)
        combo_target_detection_result_list = SingleTargetMapDetector.detect_single_target_map(current_target_map_path)
        single_target_crops = combo_target_detection_result_list[0]
        json_file = combo_target_detection_result_list[1]

        image = Image.open(current_target_map_path)
        json_file["target_map_center_location"] = (image.width / 2, image.height / 2)
        json_file["target_map_timestamp"] = get_image_timestamp_from_metadata(current_target_map_path)

        for index_in_single_target_crops in range(len(single_target_crops)):
            json_file["image_processing_results"][index_in_single_target_crops]["target_index"] = index_in_single_target_crops + 1

            current_crop_path = os.path.join(AUTONOMOUS_IMAGE_PROCESSING_SAVE_PATH, current_target_map_name + " - " + str(index_in_single_target_crops + 1) + ".png")
            single_target_crops[index_in_single_target_crops].save(current_crop_path)

            # adds target location
            target_map_center_pixel_coordinates = json_file["target_map_center_location"]
            target_pixel_coordinates = json_file["image_processing_results"][index_in_single_target_crops]["target_location"]
            target_time = json_file["target_map_timestamp"]

            closest_time_index = 0
            least_time_difference = location_log[0]["epoch_time"]

            for index in range(len(location_log)):
                difference_in_times = abs(target_time - location_log[closest_time_index]["epoch_time"])
                if difference_in_times <= least_time_difference:
                    closest_time_index = index
                    least_time_difference = difference_in_times

            drone_gps_location = location_log[closest_time_index]["current_location"]
            target_location = get_target_gps_location(target_map_center_pixel_coordinates, target_pixel_coordinates, drone_gps_location)
            target_latitude = target_location.get_lat()
            target_longitude = target_location.get_lon()

            # Check if current target is already submitted
            is_current_target_already_submitted = False

            for index in range(len(submitted_target_locations)):
                if [target_latitude, target_longitude] == submitted_target_locations[index]:
                    is_current_target_already_submitted = True
                    break

            if is_current_target_already_submitted:
                continue

            # Check if current target is outside of fly_zones
            fly_zones = construct_fly_zone_polygon(interop_client_array)
            if fly_zones.contains_point([target_latitude, target_longitude]) == 0:
                 continue

            json_file["image_processing_results"][index_in_single_target_crops]["latitude"] = target_latitude
            json_file["image_processing_results"][index_in_single_target_crops]["longitude"] = target_longitude

            shape_type = ShapeDetection.ShapeClassificationTwo(current_crop_path).get_shape_type()
            json_file["image_processing_results"][index_in_single_target_crops]["target_shape_type"] = shape_type
            color_classifying_results = Classifiers.ColorClassifier(current_crop_path).get_color()
            shape_color = color_classifying_results[0]
            letter_color = color_classifying_results[1]
            json_file["image_processing_results"][index_in_single_target_crops]["target_shape_color"] = shape_color
            json_file["image_processing_results"][index_in_single_target_crops]["target_letter_color"] = letter_color
            json_file["image_processing_results"][index_in_single_target_crops]["target_orientation"] = random.choice(["n","ne","e","se","s","sw","w","nw"])
            json_file["image_processing_results"][index_in_single_target_crops]["target_letter"] = "a"

            submitted_target_locations.append([target_latitude, target_longitude])

            interop_client_array[0].post_autonomous_target(json_file, current_crop_path, index_in_single_target_crops)

        with open(os.path.join(AUTONOMOUS_IMAGE_PROCESSING_SAVE_PATH, current_target_map_name[:-4] + ".json"), 'w') as fp:
            json.dump(json_file, fp, indent=4)
