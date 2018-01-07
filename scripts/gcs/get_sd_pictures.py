import os
import shutil
from time import sleep

SD_CARD_NAME = "NX500"
SD_PATH = os.path.join("/Volumes", SD_CARD_NAME, "DCIM")

if __name__ == '__main__':
    while True:
        print("Waiting SD Card to load...")

        if os.path.exists(SD_PATH):
            break

        sleep(0.5)

    print("SD Card loaded")

    os.system("rm static/imgs/*.jpg")
    os.system("rm static/imgs/*.JPG")

    for pic_folder in os.listdir(SD_PATH):
            pictures_dir_path = os.path.join(SD_PATH, pic_folder)
            for pic_name in os.listdir(pictures_dir_path):
                if ".JPG" in pic_name:
                    pic_path = os.path.join(pictures_dir_path, pic_name)
                    shutil.copy2(pic_path, 'static/imgs')
