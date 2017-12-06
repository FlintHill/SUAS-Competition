from flask import Flask
from flask import jsonify
from flask import send_from_directory
from flask import make_response
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
        pictures = []
        for file_name in os.listdir('imgs'):
            if file_name.endswith(".jpg"):
                pictures.append(file_name)

        return jsonify({"image_list" : pictures})
    except:
        traceback.print_exc()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8000")
