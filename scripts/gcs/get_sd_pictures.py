import os
import shutil
from time import sleep

SD_CARD_NAME = "NX500"

sd_path = os.path.join("/Volumes", SD_CARD_NAME, "DCIM")

while True:
    print("Waiting SD Card to load...")

    if os.path.exists(sd_path):
        break
    sleep(1)

print("SD Card loaded")

os.system("rm static/imgs/*.jpg")
os.system("rm static/imgs/*.JPG")

for pic_folder in os.listdir(sd_path):
        pictures_dir_path = os.path.join(sd_path, pic_folder)
        for pic_name in os.listdir(pictures_dir_path):
            if ".JPG" in pic_name:
                pic_path = os.path.join(pictures_dir_path, pic_name)
                shutil.copy2(pic_path, 'static/imgs')
