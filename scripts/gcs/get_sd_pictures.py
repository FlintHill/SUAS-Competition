import os
import shutil
from time import sleep
from SUASSystem import GCSSettings

SD_PATH = os.path.join("/Volumes", GCSSettings.SD_CARD_NAME, "DCIM")

if __name__ == '__main__':
    while True:
        print("Waiting SD Card to load...")

        if os.path.exists(SD_PATH):
            break

        sleep(1)

    print("SD Card loaded")

    os.system("rm static/all_imgs/*")
    os.system("rm static/imgs/*")
    os.system("rm static/crops/*")

    for pic_folder in os.listdir(SD_PATH):
            pictures_dir_path = os.path.join(SD_PATH, pic_folder)
            for pic_name in os.listdir(pictures_dir_path):
                if ".JPG" in pic_name:
                    pic_path = os.path.join(pictures_dir_path, pic_name)
                    shutil.copy2(pic_path, 'static/all_imgs')
