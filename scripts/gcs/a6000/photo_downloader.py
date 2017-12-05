import requests
import json
from os import walk
import shutil
import time


def startScript():

    while True:

        r = requests.get("http://10.33.20.42:8000/get/imgs")
        print (r.status_code)

        if r.status_code != 200:
            pass

        img = json.loads(r.text)

        downloaded_photos = []

        for(dirpath, dirnames, filenames) in walk("imgs"):
            downloaded_photos = filenames

        photos_to_download = []

        for i in range(0, len(img)):
            photo_to_download = list(set(img) - set(downloaded_photos))
        print('http://10.33.20.42:8000/get/imgs/' + photo_to_download[0])
        response = requests.get('http://10.33.20.42:8000/get/imgs/' + photo_to_download[0], stream=True)

        with open("imgs/" + photo_to_download[0], 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        time.sleep(4)
startScript()
