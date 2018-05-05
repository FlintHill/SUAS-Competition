from SUASSystem import GCSSettings, Location
from .utils import *
from time import sleep
import os
import shutil

def load_sd_card(location_log, interop_client_array):
    SD_PATH = os.path.join("/Volumes", GCSSettings.SD_CARD_NAME, "DCIM")

    print("Waiting SD Card to load...")

    if os.path.exists("static/all_imgs"):
        shutil.rmtree("static/all_imgs")
    os.makedirs("static/all_imgs")

    if os.path.exists("static/imgs"):
        shutil.rmtree("static/imgs")
    os.makedirs("static/imgs")

    if os.path.exists("static/crops"):
        shutil.rmtree("static/crops")
    os.makedirs("static/crops")

    if os.path.exists("static/auto_crops"):
        shutil.rmtree("static/auto_crops")
    os.makedirs("static/auto_crops")

    if os.path.exists("static/auto_imgs"):
        shutil.rmtree("static/auto_imgs")
    os.makedirs("static/auto_imgs")

    print("Cleared Image Processing folders")

    while True:

        if os.path.exists(SD_PATH):
            break

        sleep(5)

    print("SD Card loaded")

    fly_zones = construct_fly_zone_polygon(interop_client_array)
    print(fly_zones)
    print(location_log)

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
                        difference_in_times = target_time - location_log[index]["epoch_time"]
                        if abs(difference_in_times) <= least_time_difference:
                            closest_time_index = index
                            least_time_difference = difference_in_times
                    drone_gps_location = Location(location_log[closest_time_index]["latitude"], location_log[closest_time_index]["longitude"], location_log[closest_time_index]["altitude"])

                    if fly_zones.contains_point([drone_gps_location.get_lat(), drone_gps_location.get_lon()]) == 0:
                        # not in range
                        print(pic_name)
                        print(drone_gps_location.get_lat())
                        print(drone_gps_location.get_lon())
                        print("is eleminated for not being in range")
                        continue

                    if abs(drone_gps_location.get_alt() - GCSSettings.SEARCH_AREA_ALT) > 30:
                        # drone too low
                        print(pic_name)
                        print(drone_gps_location.get_alt())
                        print("is eleminated for being too low or too high")
                        continue

                    shutil.copy2(pic_path, "static/auto_imgs")
                    shutil.copy2(pic_path, "static/imgs")
                    print("successful copy")
