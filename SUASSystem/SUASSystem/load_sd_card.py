from SUASSystem import GCSSettings
from .utils import *
from time import sleep
import os
import shutil

def load_sd_card(location_log, interop_client_array):
    SD_PATH = os.path.join("/Volumes", GCSSettings.SD_CARD_NAME, "DCIM")

    while True:
        print("Waiting SD Card to load...")

        if os.path.exists(SD_PATH):
            break

        sleep(5)

    print("SD Card loaded")

    if os.path.exists("static/all_imgs"):
        shutil.rmtree("static/all_imgs")
    os.makedirs("static/all_imgs")

    if os.path.exists("static/imgs"):
        shutil.rmtree("static/imgs")
    os.makedirs("static/imgs")

    if os.path.exists("static/crops"):
        shutil.rmtree("static/crops")
    os.makedirs("static/crops")

    if os.path.exists("static/autonomous_crops"):
        shutil.rmtree("static/autonomous_crops")
    os.makedirs("static/autonomous_crops")

    fly_zones = construct_fly_zone_polygon(interop_client_array)

    for pic_folder in os.listdir(SD_PATH):
        if not "." in pic_folder:
            pictures_dir_path = os.path.join(SD_PATH, pic_folder)
            for pic_name in os.listdir(pictures_dir_path):
                if ".jpg" in pic_name.lower() and pic_name[:1] != ".":
                    pic_path = os.path.join(pictures_dir_path, pic_name)
                    shutil.copy2(pic_path, "static/all_imgs")

                    target_time = get_image_timestamp_from_metadata(pic_path)
                    closest_time_index = 0
                    least_time_difference = location_log[0]["epoch_time"]
                    for index in range(len(location_log)):
                        difference_in_times = target_time - location_log[closest_time_index]["epoch_time"]
                        if abs(difference_in_times) <= least_time_difference:
                            closest_time_index = index
                            least_time_difference = difference_in_times
                    drone_gps_location = location_log[closest_time_index]["current_location"]

                    if fly_zones.contains_point([drone_gps_location.get_lat(), drone_gps_location.get_lon()]) == 0:
                        # not in range
                        #continue
                        pass

                    shutil.copy2(pic_path, "static/imgs")
