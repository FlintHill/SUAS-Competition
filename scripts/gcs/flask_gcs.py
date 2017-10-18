from flask import Flask, render_template, redirect, url_for, jsonify, send_from_directory
import multiprocessing
import SUASSystem
import os

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    return render_template('index.html', client=client)

@app.route('/post/sda/<string:status>', methods=["POST"])
def update_sda_status(status):
    global client

    try:
        client.set_sda_status(status)

        return jsonify({"status" : "success"})
    except:
        return jsonify({"status" : "failure"})

@app.route('/get/sda', methods=["GET"])
def get_sda_status():
    global client

    data = {
        "status" : client.get_sda_status()
    }

    return jsonify(data)

@app.route('/get/img_proc', methods=["GET"])
def get_img_proc_status():
    global client

    data = {
        "status" : client.get_img_proc_status()
    }

    return jsonify(data)

@app.route('/post/img_proc/<string:status>', methods=["POST"])
def update_img_proc_status(status):
    global client

    try:
        client.set_img_proc_status(status)

        return jsonify({"status" : "success"})
    except:
        return jsonify({"status" : "failure"})

@app.route('/get/interop', methods=["GET"])
def get_interop_position_update_rate():
    global client

    return jsonify(client.interop_data[0])

@app.route('/imgs/<path:path>', methods=["GET"])
def get_image(path):
    return send_from_directory('static/imgs', path)

@app.route('/get/imgs', methods=["GET"])
def get_image_list():
    pictures = {}
    picture_index = 0
    for file_name in os.listdir('static/imgs'):
        if file_name.endswith(".jpg"):
            pictures[picture_index] = file_name
            picture_index = picture_index + 1

    return jsonify(pictures)

class Client(object):

    def __init__(self):
        self.manager = multiprocessing.Manager()
        self.sda_status = self.manager.Value('s', "disconnected")
        self.img_proc_status = self.manager.Value('s', "disconnected")

        self.interop_client = self.manager.list()
        #self.interop_client.append(SUASSystem.InteropClientConverter())
        self.interop_data = self.manager.list()
        self.interop_data.append(self.get_interop_data())

        self.gcs_process = multiprocessing.Process(target=SUASSystem.gcs_process, args=(
            self.sda_status,
            self.img_proc_status,
            self.interop_client
        ))
        #self.gcs_process.start()

    def get_interop_data(self):
        try:
            active_interop_mission = self.interop_client[0].get_active_mission()
            obtstacles = self.interop_client[0].get_obstacles()
            active_interop_mission_json = SUASSystem.get_mission_json(active_interop_mission, obstacles)

            data = {
                "status": "connected",
                "emergent_position": [
                    active_interop_mission_json["emergent_last_known_pos"]["latitude"],
                    active_interop_mission_json["emergent_last_known_pos"]["longitude"]
                ],
                "airdrop_position": [
                    active_interop_mission_json["air_drop_pos"]["latitude"],
                    active_interop_mission_json["air_drop_pos"]["longitude"]
                ],
                "off-axis_position": [
                    active_interop_mission_json["off_axis_target_pos"]["latitude"],
                    active_interop_mission_json["off_axis_target_pos"]["longitude"]
                ]
            }
        except:
            data = {
                "status": "disconnected",
                "emergent_position": [0, 0],
                "airdrop_position": [0, 0],
                "off-axis_position": [0, 0]
            }

        return data

    def set_sda_status(self, status):
        self.sda_status.value = status

    def get_sda_status(self):
        return self.sda_status.value

    def set_img_proc_status(self, status):
        self.img_proc_status.value = status

    def get_img_proc_status(self):
        return self.img_proc_status.value

client = Client()
