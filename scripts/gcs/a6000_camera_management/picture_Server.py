from flask import Flask, jsonify, send_from_directory, make_response
import traceback
import os

app = Flask(__name__)
@app.route('/get/imgs/<path:path>', methods=["GET"])
def get_image(path):
    try:
        return send_from_directory('imgs', path)
    except:
        traceback.print_exc()

@app.route('/get/imgs', methods=["GET"])
def get_image_list():
    try:
        pictures = {}
        pictures_index = 0
        for file_name in os.listdir('imgs'):
            if file_name.endswith(".jpg"):
                pictures[pictures_index] = file_name
                pictures_index = pictures_index + 1
        return jsonify(pictures)
    except:
        traceback.print_exc()


if __name__ == '__main__':
    app.run(host="0.0.0.0")
