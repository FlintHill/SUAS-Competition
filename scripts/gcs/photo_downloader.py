import requests
import json
import traceback
import os
import shutil
from time import sleep

ODROID_IP_ADDRESS = "10.33.20.42"
GET_IMG_LIST_API = "http://" + ODROID_IP_ADDRESS + ":8000/get/imgs"
DOWNLOAD_IMAGE_API = "http://" + ODROID_IP_ADDRESS + ":8000/get/imgs/"
IMAGES_DIRECTORY = "static/imgs"

def download_images():
    while True:
        try:
            img_list_response = requests.get(GET_IMG_LIST_API)
            img_list = json.loads(img_list_response.json)["image_list"]

            _, __, already_downloaded_photos = os.walk(IMAGES_DIRECTORY)
            photos_to_download = list(set(img_list) - set(already_downloaded_photos))

            response = requests.get(DOWNLOAD_IMAGE_API + photos_to_download[0], stream=True)
            with open(os.path.join(IMAGES_DIRECTORY + photo_to_download[0]), 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)

            sleep(1)
        except:
            traceback.print_exc()

if __name__ == '__main__':
    download_images()
