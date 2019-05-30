from flask import Flask, render_template, redirect, url_for, jsonify, send_from_directory, request
import multiprocessing
import SUASSystem
from SUASSystem import utils
from datetime import datetime
import os
import json
import traceback

"""
run this file in order to execute our code base through flask which is a python framework, similar to Django in that sense, but is lightweight
and better suits API development. Makes calls to other files in the code base, including the gcs.py file which performs all necessary operations for compeition.
"""

class Client(object):

	def __init__(self):
		self.manager = multiprocessing.Manager()
		self.sda_status = self.manager.Value('s', "disconnected")
		self.img_proc_status = self.manager.Value('s', "disconnected")
		self.sda_start_time = self.manager.Value('i', int(datetime.utcnow().strftime("%s")))
		self.img_proc_start_time = self.manager.Value('i', int(datetime.utcnow().strftime("%s")))
		self.targets_to_submit = self.manager.list()
		self.autonomous_targets_to_submit = self.manager.list()
		self.location_log = self.manager.list()

		self.interop_client = self.manager.list()
		self.interop_client.append(SUASSystem.InteropClientConverter())
		self.interop_data = self.manager.list()
		self.interop_data.append(self.get_interop_data())

		#call to the gcs.py file.
		print("got to gcs process call in flask_gcs")
		self.gcs_process = multiprocessing.Process(target=SUASSystem.gcs_process, args=(
			self.sda_status,
			self.img_proc_status,
			self.interop_client,
			self.targets_to_submit,
			self.location_log,
			self.autonomous_targets_to_submit
		))
		self.gcs_process.start()

	def get_location_log(self):
		"""
		gets log of UAV loaction data in Json format
		"""
		return list(self.location_log)

	def submit_autonomous_target(self, target):

		"""
		gets targets identififed autonomously for image processing.
		"""
		self.autonomous_targets_to_submit.append(target)

	def get_interop_data(self):
		"""
		gets Json data on vehicle posiion needed for interop.
		"""
		try:
			active_interop_mission = self.interop_client[0].get_active_mission()
			print(active_interop_mission)
			obstacles = self.interop_client[0].get_obstacles()
			print("in flask_gcs")
			print( len(obstacles))
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
				],
				"search_grid_points": [
			        {
			            "latitude" : search_grid_point["latitude"],
			            "longitude" : search_grid_point["longitude"],
			            "order" : search_grid_point["order"]
			        } for search_grid_point in active_interop_mission_json["search_grid_points"]
			    ]
			}

		except:
			data = {
				"status": "disconnected",
				"emergent_position": [0, 0],
				"airdrop_position": [0, 0],
				"off-axis_position": [0, 0],
				"search_grid_points": []
			}

		return data

	def set_sda_status(self, status):
		if status == "connected":
			self.sda_start_time.value = int(datetime.utcnow().strftime("%s"))

		self.sda_status.value = status

	def get_sda_status(self):
		return self.sda_status.value

	def set_img_proc_status(self, status):
		if status == "connected":
			self.img_proc_start_time.value = int(datetime.utcnow().strftime("%s"))

		self.img_proc_status.value = status

	def get_img_proc_status(self):
		return self.img_proc_status.value

app = Flask(__name__, static_url_path='')
client = Client()

@app.after_request
def add_header(r):
	"""
	Add headers to both force latest IE rendering engine or Chrome Frameself.
	"""
	r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	r.headers["Pragma"] = "no-cache"
	r.headers["Expires"] = "0"
	r.headers['Cache-Control'] = 'public, max-age=0'

	return r

@app.route('/')
def index():
	try:
		return render_template('index.html', client=client)
	except:
		traceback.print_exc()

@app.route('/get/uav_location_log', methods=["GET"])
def get_uav_location_log():
	#gets UAV location formatted in Json data. Essentially makes call to get_location_log method
	try:
		return jsonify({"request_status" : "success", "location_log" : client.get_location_log()})
	except:
		traceback.print_exc()

		return jsonify({"request_status" : "failure"})

@app.route('/post/autonomous_img_proc_target', methods=["POST"])
def update_auto_img_proc_status():
	try:
		client.submit_autonomous_target(request.json)

		return jsonify({"request_status" : "success"})
	except:
		traceback.print_exc()

		return jsonify({"request_status" : "failure"})

@app.route('/get/offset', methods=["GET"])
def update_offset():
	try:
		return jsonify({"request_status" : "success", "offset": SUASSystem.GCSSettings.CAMERA_NORTH_OFFSET})
	except:
		traceback.print_exc()

		return jsonify({"request_status" : "failure"})

@app.route('/post/sda/<string:status>', methods=["POST"])
def update_sda_status(status):
	try:
		client.set_sda_status(status)

		return jsonify({"request_status" : "success"})
	except:
		traceback.print_exc()

		return jsonify({"request_status" : "failure"})

@app.route('/get/sda', methods=["GET", "POST"])
def get_sda_status():
	try:
		sda_runtime = int(datetime.utcnow().strftime("%s")) - client.sda_start_time.value
		minutes = sda_runtime / 60
		seconds = sda_runtime % 60
		sda_runtime_string = str(minutes) + " mins, " + str(seconds) + " secs"

		data = {
			"status" : client.get_sda_status(),
			"runtime" : sda_runtime_string,
			"request_status" : "success"
		}

		return jsonify(data)
	except:
		traceback.print_exc()

		data = {
			"request_status" : "failure"
		}

		return jsonify(data)

@app.route('/get/img_proc', methods=["GET", "POST"])
def get_img_proc_status():
	try:
		img_proc_runtime = int(datetime.utcnow().strftime("%s")) - client.img_proc_start_time.value
		minutes = img_proc_runtime / 60
		seconds = img_proc_runtime % 60
		img_proc_runtime_string = str(minutes) + " mins, " + str(seconds) + " secs"

		data = {
			"status" : client.get_img_proc_status(),
			"runtime" : img_proc_runtime_string,
			"request_status" : "success"
		}

		return jsonify(data)
	except:
		traceback.print_exc()

		data = {
			"request_status" : "failure"
		}

		return jsonify(data)

@app.route('/post/img_proc/<string:status>', methods=["POST"])
def update_img_proc_status(status):
	try:
		client.set_img_proc_status(status)

		return jsonify({"request_status" : "success"})
	except:
		traceback.print_exc()

		return jsonify({"request_status" : "failure"})

@app.route('/get/interop', methods=["GET", "POST"])
def get_interop_position_update_rate():
	try:
		return jsonify(client.interop_data[0])
	except:
		traceback.print_exc()

		data = {
			"request_status" : "failure"
		}

		return jsonify(data)

@app.route('/get/crop/<path:path>', methods=["GET", "POST"])
def get_crop(path):
	try:
		return send_from_directory('static/crops', path)
	except:
		traceback.print_exc()

@app.route('/get/imgs/<path:path>', methods=["GET", "POST"])
def get_image(path):
	try:
		return send_from_directory('static/imgs', path)
	except:
		traceback.print_exc()

@app.route('/get/imgs', methods=["GET", "POST"])
def get_image_list():
	try:
		pictures = {}
		picture_index = 0
		for file_name in os.listdir('static/imgs'):
			if is_file_an_image(file_name):
				pictures[picture_index] = file_name
				picture_index = picture_index + 1

		return jsonify(pictures)
	except:
		traceback.print_exc()

def is_file_an_image(file_name):
	image_file_types = [".JPG", ".JPEG", ".jpg"]

	for file_type in image_file_types:
		if file_type in file_name:
			return True

	return False

@app.route('/post/target', methods=["POST"])
def post_target():
	try:
		# check for duplicates
		submitted_target_characteristics = [];

		path_to_json = 'static/crops/'
		submitted_json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

		for json_file in submitted_json_files:
			json_data = {"id": json_file[0:json_file.find(".")]}
			json_data.update(json.load(open("static/crops/" + json_file)))

			submitted_target_characteristics.append(json_data)

		targets_with_similar_characteristics = []

		for target in submitted_target_characteristics:
			matched_characteristics = 0

			if request.form["type"] == "standard":
				if target["type"] != "standard":
					continue

				if target["shape"] == request.form["targetShape"]:
					matched_characteristics += 1
				if target["background_color"] == request.form["targetColor"]:
					matched_characteristics += 1
				if target["alphanumeric_color"] == request.form["contentColor"]:
					matched_characteristics += 1
				if target["alphanumeric"] == request.form["targetContent"]:
					matched_characteristics += 1
			elif target["type"] == "emergent":
				matched_characteristics += 1

			if matched_characteristics > 0:
				if target["type"] == "standard":
					targets_with_similar_characteristics.append({
						"name": ("target" + ("%03d" % (int(target["id"]),)) ),
						"matches": matched_characteristics,

						"type": "standard",

						"imageURL": "get/crop/" + target["id"] + ".jpg",
						"geo": str(target["latitude"]) + ", " + str(target["longitude"]),
						"shape": target["shape"],
						"shapeColor": target["background_color"],
						"textColor": target["alphanumeric_color"],
						"alphanumeric": target["alphanumeric"]
					})
				if target["type"] == "emergent":
					targets_with_similar_characteristics.append({
						"name": ("target" + ("%03d" % (int(target["id"]),)) ),
						"matches": matched_characteristics,

						"type": "emergent",

						"imageURL": "get/crop/" + target["id"] + ".jpg",
						"geo": str(target["latitude"]) + ", " + str(target["longitude"]),
					})

		if len(targets_with_similar_characteristics) > 0 and request.form["ignoreDuplicates"] == "false": # ask user to confirm
			targets_with_similar_characteristics.append({"duplicatesPossible": "true"})

			return jsonify(targets_with_similar_characteristics)

		# create and submit target data to be cropped
		if request.form["type"] == "standard":
			target_characteristics = {
				"type" : "standard",
				"alphanumeric" : request.form["targetContent"],
				"alphanumeric_color" : request.form["contentColor"],
				"shape" : request.form["targetShape"],
				"orientation" : request.form["targetOrientation"],
				"base_image_filename" : request.form["imageFilename"],
				"background_color" : request.form["targetColor"],
				"target_top_left" : [int(request.form["targetTopLeftX"]), int(request.form["targetTopLeftY"])],
				"target_bottom_right" : [int(request.form["targetBottomRightX"]), int(request.form["targetBottomRightY"])],
				"latitude" : 0,
				"longitude" : 0
			}
		else: # emergent target
			target_characteristics = {
				"type" : request.form["type"],
				"emergent_description" : request.form["description"],
				"base_image_filename" : request.form["imageFilename"],
				"target_top_left" : [int(request.form["targetTopLeftX"]), int(request.form["targetTopLeftY"])],
				"target_bottom_right" : [int(request.form["targetBottomRightX"]), int(request.form["targetBottomRightY"])],
				"latitude" : 0,
				"longitude" : 0
			}

		client.targets_to_submit.append(target_characteristics)

		return jsonify({"request_status" : "success"})
	except:
		traceback.print_exc()

		return jsonify({"request_status" : "failure"})

app.config["CACHE_TYPE"] = "null"
app.run(host="0.0.0.0")
