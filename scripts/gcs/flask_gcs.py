from flask import Flask, render_template, redirect, url_for, jsonify
import multiprocessing
import SUASSystem

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', client=client)

@app.route('/post/sda/<string:status>')
def update_sda_status(status):
    global client
    client.set_sda_status(status)

    return redirect(url_for('index'))

@app.route('/post/img_proc/<string:status>')
def update_img_proc_status(status):
    global client
    client.set_img_proc_status(status)

    return redirect(url_for('index'))

@app.route('/interop/get_interop_position_update_rate')
def get_interop_position_update_rate():
    return jsonify(result=client.get_interop_position_update_rate())

class Client(object):

    def __init__(self):
        self.manager = multiprocessing.Manager()
        self.sda_status = self.manager.Value('s', "Disabled")
        self.img_proc_status = self.manager.Value('s', "Disabled")
        self.interop_position_update_rate = self.manager.Value('i', 2.00)

        self.gcs_process = multiprocessing.Process(target=SUASSystem.gcs_process, args=(
            self.sda_status,
            self.img_proc_status,
            self.interop_position_update_rate,
        ))
        self.gcs_process.start()

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
