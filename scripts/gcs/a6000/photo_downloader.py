import requests
import json
import os
import shutil


while True:
    r = requests.get("http://0.0.0.0:5000/get/imgs")
    imgs = json.load(r.text)

    downloaded_photos = []

    for(dirpath, dirnames, filenames) in walk(img):
        downloaded_photos = filenames

    photos_to_download = []

    for i in range(0, len(imgs)):
        photo_to_download = list(set(imgs) - set(downloaded_photos))

    for image in photos_to_download:
        response = requests.get('http://odroid@INPUT_PORT/get/imgs/' + image, stream=True)

        with open(image, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)

        del response
