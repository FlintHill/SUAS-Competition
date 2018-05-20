from UpdatedImageProcessing import *
from SUASSystem.utils import *
import requests
import json
from SUASSystem import Location
import matplotlib
from time import sleep
import random

def autonomous_image_processing():
    TARGET_MAP_PATH = "../../scripts/gcs/static/auto_imgs/"
    AUTONOMOUS_IMAGE_PROCESSING_SAVE_PATH = "../../scripts/gcs/static/auto_crops/"
    SAVE_PATH_FOR_POSTING = "static/auto_crops/"

    processed_target_maps = []
    while True:
        sleep(1)
        try:
            map_list_response = requests.get("http://localhost:5000/get/imgs")
            target_map_list = map_list_response.json()
            needs_refresh = False
        except:
            continue

        interop_response = requests.get("http://localhost:5000/get/interop")
        interop_json = interop_response.json()
        fly_zones = construct_fly_zone_polygon_from_json(interop_json)
        runway_zone, runway_grass1_zone, runway_grass2_zone, runway_grass3_zone, runway_grass4_zone, runway_grass5_zone = construct_runway_fly_zone():

        location_log_response = requests.get("http://localhost:5000/get/uav_location_log")
        location_log = location_log_response.json()["location_log"]

        for map_index in range(len(target_map_list)):
            if target_map_list[str(map_index)] in processed_target_maps:
                if map_index + 1 == len(target_map_list):
                    needs_refresh = True
                continue
            else:
                current_target_map_name = target_map_list[str(map_index)]
                processed_target_maps.append(current_target_map_name)
                break

        if len(target_map_list) == 0 or needs_refresh:
            continue

        current_target_map_path = os.path.join(TARGET_MAP_PATH, current_target_map_name)
        combo_target_detection_result_list = SingleTargetMapDetector.detect_single_target_map(current_target_map_path)

        single_target_crops = combo_target_detection_result_list[0]
        json_file = combo_target_detection_result_list[1]

        image = Image.open(current_target_map_path)
        json_file["target_map_center_location"] = (image.width / 2, image.height / 2)
        json_file["target_map_timestamp"] = get_image_timestamp_from_metadata(current_target_map_path)

        print("Identifying targets within %s" % current_target_map_name)
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

            drone_gps_location = Location(location_log[closest_time_index]["latitude"], location_log[closest_time_index]["longitude"], location_log[closest_time_index]["altitude"])
            target_location = get_target_gps_location(target_map_center_pixel_coordinates, target_pixel_coordinates, drone_gps_location)

            # check if target is in fly zones
            if fly_zones.contains_point([target_location.get_lat(), target_location.get_lon()]) == 0:
                print("target eleminated -- not in range")
                continue

            # check if target is in runway or runway grass. if on runway, eleminate, if on grass, do not eleminate
            if runway_zone.contains_point([drone_gps_location.get_lat(), drone_gps_location.get_lon()]):
                # target in runway zone -- check if on grass
                if runway_grass1_zone.contains_point([drone_gps_location.get_lat(), drone_gps_location.get_lon()]):
                    pass
                elif runway_grass2_zone.contains_point([drone_gps_location.get_lat(), drone_gps_location.get_lon()]):
                    pass
                elif runway_grass3_zone.contains_point([drone_gps_location.get_lat(), drone_gps_location.get_lon()]):
                    pass
                elif runway_grass4_zone.contains_point([drone_gps_location.get_lat(), drone_gps_location.get_lon()]):
                    pass
                elif runway_grass5_zone.contains_point([drone_gps_location.get_lat(), drone_gps_location.get_lon()]):
                    pass
                else:
                    # target not in grass; must be on runway -- eleminate
                    continue

            json_file["image_processing_results"][index_in_single_target_crops]["latitude"] = target_location.get_lat()
            json_file["image_processing_results"][index_in_single_target_crops]["longitude"] = target_location.get_lon()

            shape_type = ShapeDetection.ShapeClassificationTwo(current_crop_path).get_shape_type()
            json_file["image_processing_results"][index_in_single_target_crops]["target_shape_type"] = shape_type
            color_classifying_results = Classifiers.ColorClassifier(current_crop_path).get_color()
            shape_color = color_classifying_results[0]
            letter_color = color_classifying_results[1]
            letter = "a"
            orientation = random.choice(["n","ne","e","se","s","sw","w","nw"])
            json_file["image_processing_results"][index_in_single_target_crops]["target_shape_color"] = shape_color
            json_file["image_processing_results"][index_in_single_target_crops]["target_letter_color"] = letter_color
            json_file["image_processing_results"][index_in_single_target_crops]["target_orientation"] = orientation
            json_file["image_processing_results"][index_in_single_target_crops]["target_letter"] = letter
            # create the specific target post
            posting_json = {}
            posting_json["target"] = []
            posting_json["target"].append({
                 "target_shape_color": shape_color,
                 "target_letter_color": letter_color,
                 "target_shape_type": shape_type,
                 "target_orientation": orientation,
                 "target_letter": letter,
                 "latitude": target_location.get_lat(),
                 "longitude": target_location.get_lon(),
                 "current_crop_path": os.path.join(SAVE_PATH_FOR_POSTING, current_target_map_name + " - " + str(index_in_single_target_crops + 1) + ".png")
            })
            requests.post("http://localhost:5000/post/autonomous_img_proc_target", json=posting_json)
            print("posted a %s %s" % (shape_color, shape_type))

        with open(os.path.join(AUTONOMOUS_IMAGE_PROCESSING_SAVE_PATH, current_target_map_name[:-4] + ".json"), 'w') as fp:
            json.dump(json_file, fp, indent=4)

if __name__ == "__main__":
    autonomous_image_processing()
