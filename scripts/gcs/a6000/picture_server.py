from flask import Flask
from flask import jsonify
from flask import send_from_directory
import multiprocessing
import subprocess
import traceback
import os
from time import sleep
from datetime import datetime

app = Flask(__name__)

IMAGE_DIRECTORY_PATH = "imgs"
DELAY_BETWEEN_PICTURES_IN_SECONDS = 4

@app.route('/get/imgs/<path:path>', methods=["GET"])
def get_image(path):
    try:
        return send_from_directory('imgs', path)
    except:
        traceback.print_exc()

@app.route('/get/imgs', methods=["GET"])
def get_image_list():
    try:
        pictures = []
        for file_name in os.listdir(IMAGE_DIRECTORY_PATH):
            if file_name.endswith(".jpg"):
                pictures.append(file_name)

        return jsonify({"image_list" : pictures})
    except:
        traceback.print_exc()

def take_pictures():
    while True:
        time = str(datetime.utcnow().strftime("%s"))
        subprocess.call("gphoto2", "--capture-image-and-download", "--filename", "image-" + time + ".jpg")

        sleep(DELAY_BETWEEN_PICTURES_IN_SECONDS)

def create_picture_taking_process():
    picture_taking_process = multiprocessing.Process(target=take_pictures)
    picture_taking_process.start()

    return picture_taking_process

def is_process_dead(child_process):
    if child_process.poll() is None:
        return False

    return True

def is_image_directory_changing(previous_image_directory_contents):
    if len(list(set(os.listdir(IMAGE_DIRECTORY_PATH)) - set(previous_image_directory_contents))) == 0:
        return False

    return True

def manage_camera():
    picture_taking_process = create_picture_taking_process()
    sleep(20)
    previous_image_directory_contents = os.listdir(IMAGE_DIRECTORY_PATH)

    while True:
        print(previous_image_directory_contents)
        if is_process_dead(picture_taking_process) or is_image_directory_changing(previous_image_directory_contents):
            print("[Error] Camera image gathering process is not working...Rebooting...")

            picture_taking_process.kill()
            sleep(10)
            picture_taking_process = create_picture_taking_process()

        previous_image_directory_contents = os.listdir(IMAGE_DIRECTORY_PATH)
        sleep(20)

if __name__ == '__main__':
    camera_manager_process = multiprocessing.Process(target=manage_camera)
    camera_manager_process.start()

    app.run(host="0.0.0.0", port="8000")
