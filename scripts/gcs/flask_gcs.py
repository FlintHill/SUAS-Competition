from flask import Flask, render_template, redirect, url_for, jsonify, send_from_directory
import multiprocessing
import SUASSystem
import os

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    return render_template('index.html', client=client)

@app.route('/post/sda/<string:status>')
def update_sda_status(status):
    global client

    try:
        client.set_sda_status(status)

        return jsonify({"status" : "success"})
    except:
        return jsonify({"status" : "failure"})

@app.route('/post/img_proc/<string:status>')
def update_img_proc_status(status):
    global client

    try:
        client.set_img_proc_status(status)

        return jsonify({"status" : "success"})
    except:
        return jsonify({"status" : "failure"})

@app.route('/interop/get_interop_position_update_rate')
def get_interop_position_update_rate():
    return jsonify(result=client.get_interop_position_update_rate())

@app.route('/imgs/<path:path>')
def get_image(path):
    return send_from_directory('static/imgs', path)

@app.route('/get/imgs')
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
        self.sda_status = self.manager.Value('s', "Disabled")
        self.img_proc_status = self.manager.Value('s', "Disabled")
        self.interop_position_update_rate = self.manager.Value('i', 2.00)
        self.interop_client = self.manager.list()
        #self.interop_client.append(SUASSystem.InteropClientConverter())

        self.gcs_process = multiprocessing.Process(target=SUASSystem.gcs_process, args=(
            self.sda_status,
            self.img_proc_status,
            self.interop_position_update_rate,
            self.interop_client
        ))
        #self.gcs_process.start()

    def set_sda_status(self, status):
        self.sda_status.value = status

    def get_sda_status(self):
        return self.sda_status.value

    def set_img_proc_status(self, status):
        self.img_proc_status.value = status

    def get_img_proc_status(self):
        return self.img_proc_status.value

    def set_interop_position_update_rate(self, rate):
        self.interop_position_update_rate.value = rate

    def get_interop_position_update_rate(self):
        return self.interop_position_update_rate.value

client = Client()
