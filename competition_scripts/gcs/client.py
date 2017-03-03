import socket
import multiprocessing
import sys
import json
import os
import math
import numpy as np
from logger import *
from datetime import datetime
from time import sleep
from interop_client import InteropClientConverter
from obstacle_container import ObstacleContainer
from static_math import haversine, bearing
from current_coordinates import CurrentCoordinates
from converter_data_update import ConverterDataUpdate
from ClientConverter import ClientConverter
from obstacle import Obstacle
from waypoint import Waypoint
from message import Message
from ObjAvoid import *

INTEROP_CLIENT_ADDRESS = ('localhost', 9000)
TK1_ADDRESS = ('IP', 9001)
send_course_max_port = 10020
server_address = 'localhost'
waypoint_JSON_file_path = "./data/demo_waypoints.mission"

INTEROP_URL = "http://10.10.130.2:8000"
INTEROP_USERNAME = "Flint"
INTEROP_PASSWORD = "2429875295"
MSL = 22

def send_data(connection, data):
	connection.sendall(data)

def send_course(logger_queue, configurer, input_pipe):
	"""
	Send course to mission planner instance

	:param output_pipe: The data to send to the mission planner instances
		goes through this pipe
	"""
	configurer(logger_queue)
	name = multiprocessing.current_process().name

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	is_connected = False
	port = send_course_max_port

	sleep(10)

	while not is_connected:
		try:
			log(name, "Connecting to send_course socket on port " + str(port) + "...")
			sock.connect((server_address, port))

			is_connected = True
		except:
			log(name, "Socket for send_course is not open...")
			sleep(0.1)

			port -= 1
			if port < send_course_max_port - 10:
				port = send_course_max_port
	log(name, "Connected to send_course socket")

	while True:
		if input_pipe.poll():
			data = input_pipe.recv()

			log(name, "Sending telem to send_course socket: " + str(data))
			send_data(sock, data.encode())
		else:
			pass

		sleep(0.05)

def receive_targets(logger_queue, configurer, received_targets_array):
	"""
	Receive the targets from the TK1
	"""
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#sock.bind(TK1_ADDRESS)
	#sock.listen(1)
	log(name, "Waiting for a connection to the TK1...")
	#connection, client_address = sock.accept()
	log(name, "Connected to TK1")

	while True:
		sleep(0.5)

def receive_telem(logger_queue, configurer, receive_telem_array):
	"""
	Receive telemetry from the local mission planner instance

	:param current_coordinates_array: The multiprocessing list to use to
		store received telem data from mission planner
	"""
	configurer(logger_queue)
	name = multiprocessing.current_process().name
	logger = logging.getLogger(name)

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('localhost', 10000)
	sock.bind(server_address)
	sock.listen(1)
	log(name, "Waiting for a connection to MP...")
	connection, client_address = sock.accept()
	log(name, "Connected to MP")

	while True:
		curr_coords = {
			"lat" : -1.0,
			"lng" : -1.0,
			"alt" : -1.0,
			"heading" : -1
		}

		previous_message = None
		while curr_coords["lat"] == -1.0 or curr_coords["lng"] == -1.0 or curr_coords["alt"] == -1.0 or curr_coords["heading"] == -1:
			data = connection.recv(64).decode("utf-8")

			messages = data.split(" ")
			for index in range(len(messages) - 1):
				if previous_message:
					curr_coords[previous_message] = float(messages[index])
					previous_message = None
				elif messages[index] in curr_coords:
					previous_message = messages[index]

		log(name, str(curr_coords))
		curr_coords["heading"] /= (2 * math.pi)
		receive_telem_array[0] = CurrentCoordinates(curr_coords["lat"], curr_coords["lng"], curr_coords["alt"], curr_coords["heading"])

if __name__ == '__main__':
	interop_server_client = InteropClientConverter(MSL, INTEROP_URL, INTEROP_USERNAME, INTEROP_PASSWORD)

	logger_queue = multiprocessing.Queue(-1)
	logger_listener_process = multiprocessing.Process(target=listener_process, args=(logger_queue, logger_listener_configurer))
	logger_listener_process.start()

	manager = multiprocessing.Manager()

	current_coordinates = manager.list()
	current_coordinates.extend([CurrentCoordinates(0.0, 0.0, 0.0, 0.0)])
	current_obstacles = manager.list()
	current_obstacles.extend([ObstacleContainer([], [])])

	guided_waypoint_input, guided_waypoint_output = multiprocessing.Pipe()

	telem_process = multiprocessing.Process(target=receive_telem, args=(logger_queue, logger_worker_configurer, current_coordinates,))
	telem_process.start()

	send_course_process = multiprocessing.Process(target=send_course, args=(logger_queue, logger_worker_configurer, guided_waypoint_input,))
	send_course_process.start()

	waypoints = json.load(open(waypoint_JSON_file_path, 'r'))["items"]
	waypoints_list = []
	for json_waypoint in waypoints:
		if json_waypoint["coordinate"][0] != 0.0:
			waypoints_list.append(Waypoint(json_waypoint["coordinate"][0], json_waypoint["coordinate"][1], json_waypoint["coordinate"][2]))

	while current_coordinates[0].get_latitude() == 0.0:
		sleep(0.05)

	obstacle_map = ClientConverter(current_coordinates[0].as_gps())
	obstacle_map.set_waypoints(waypoints_list)

	while True:
		start_time = datetime.now()
		interop_server_client.post_telemetry(CurrentCoordinates(1.0, 1.0, 1.0, 180))
		obstacles = ObstacleContainer(interop_server_client.get_obstacles())

		initialCoords = obstacle_map.get_initial_coordinates()
		haversine_distance = haversine(initialCoords, current_coordinates[0].as_gps())
		updated_drone_location = ConverterDataUpdate(haversine_distance, current_coordinates[0].get_heading(), current_coordinates[0].get_altitude())
		obj_avoid_coordinates = obstacle_map.update_drone_mass_position(updated_drone_location)

		if obj_avoid_coordinates and current_coordinates[0].get_altitude() > 7:
			log("root", "Sending avoid coordinates...")
			guided_waypoint_output.send("lat " + str(obj_avoid_coordinates.get_latitude()) + " ")
			guided_waypoint_output.send("lng " + str(obj_avoid_coordinates.get_longitude()) + " ")
			guided_waypoint_output.send("alt " + str(current_coordinates[0].get_altitude()) + " ")

		time_to_execute = (datetime.now() - start_time).seconds
		print("time_to_execute: " + str(time_to_execute))
		sleep(1 - time_to_execute)
