import socket
import multiprocessing
import sys
import json
import os
import logging
import logging.handlers
from time import sleep
from static_math import haversine, bearing
from current_coordinates import CurrentCoordinates
from converter_data_update import ConverterDataUpdate
from ClientConverter import ClientConverter
from obstacle import Obstacle
from waypoint import Waypoint
from message import Message

INTEROP_CLIENT_ADDRESS = ('localhost', 9000)
server_address = 'localhost'
waypoint_JSON_file_path = "./data/demo_waypoints.mission"
log_file = "./data/log.log"

logging.basicConfig(format="%(asctime)s %(name)s [%(levelname)s] %(message)s",
	filename=log_file, filemode='w',
	level=logging.INFO)

class QueueHandler(logging.Handler):
    """
    This is a logging handler which sends events to a multiprocessing queue.

    The plan is to add it to Python 3.2, but this can be copy pasted into
    user code for use with earlier Python versions.
    """

    def __init__(self, queue):
        """
        Initialise an instance, using the passed queue.
        """
        logging.Handler.__init__(self)
        self.queue = queue

    def emit(self, record):
        """
        Emit a record.

        Writes the LogRecord to the queue.
        """
        try:
            ei = record.exc_info
            if ei:
                dummy = self.format(record) # just to get traceback text into record.exc_text
                record.exc_info = None  # not needed any more
            self.queue.put_nowait(record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

def logger_listener_configurer():
    root = logging.getLogger()
    h = logging.handlers.RotatingFileHandler(log_file, 'w')
    f = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s')
    h.setFormatter(f)
    root.addHandler(h)

def logger_worker_configurer(queue):
    h = QueueHandler(queue)  # Just the one handler needed
    root = logging.getLogger()
    root.addHandler(h)
    # send all messages, for demo; no other level or filter logic applied.
    root.setLevel(logging.INFO)

def listener_process(queue, configurer):
    configurer()
    while True:
        try:
            record = queue.get()
            if record is None:  # We send this as a sentinel to tell the listener to quit.
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)  # No level or filter logic applied - just do it!
        except Exception:
            import sys, traceback
            print('Whoops! Problem:')
            traceback.print_exc(file=sys.stderr)

def send_data(connection, data):
	connection.sendall(data)

def obj_receive(logger_queue, configurer, object_array):
	"""
	Receive obstacles from the interoperability server

	:param object_array: The multiprocessing list to use to store obstacles
		from interop server
	"""
	configurer(logger_queue)
	name = multiprocessing.current_process().name
	logger = logging.getLogger(name)

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(INTEROP_CLIENT_ADDRESS)
	sock.listen(1)
	logger.info("Waiting for a connection to INTEROP_CLIENT...")
	connection, client_address = sock.accept()
	logger.info("Connected to INTEROP_CLIENT")

	while True:
		sleep(0.5)

def send_course(logger_queue, configurer, input_pipe):
	"""
	Send course to mission planner instance

	:param output_pipe: The data to send to the mission planner instances
		goes through this pipe
	"""
	configurer(logger_queue)
	name = multiprocessing.current_process().name
	logger = logging.getLogger(name)

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	is_connected = False
	port = 10010

	sleep(10)

	while not is_connected:
		try:
			logger.info("Connecting to send_course socket on port " + str(port) + "...")
			sock.connect((server_address, port))

			is_connected = True
		except:
			logger.info("Socket for send_course is not open...")
			sleep(0.1)

			port -= 1
			if port < 10000:
				port = 10010
	logger.info("Connected to send_course socket")

	while True:
		if input_pipe.poll():
			data = input_pipe.recv()

			logger.info("Sending telem to send_course socket: " + str(data))
			send_data(sock, data.encode())
		else:
			pass

		sleep(0.05)

def receive_telem(logger_queue, configurer, current_coordinates_array):
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
	logger.info("Waiting for a connection to MP...")
	connection, client_address = sock.accept()
	logger.info("Connected to MP")

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

		logger.info(str(curr_coords))
		current_coordinates_array[0] = CurrentCoordinates(curr_coords["lat"], curr_coords["lng"], curr_coords["alt"], curr_coords["heading"])

if __name__ == '__main__':
	logger_queue = multiprocessing.Queue(-1)
	logger_listener_process = multiprocessing.Process(target=listener_process, args=(logger_queue, logger_listener_configurer))
	logger_listener_process.start()

	manager = multiprocessing.Manager()

	current_coordinates = manager.list()
	current_coordinates.extend([CurrentCoordinates(0.0, 0.0, 0.0, 0.0)])
	current_obstacles = manager.list()

	guided_waypoint_input, guided_waypoint_output = multiprocessing.Pipe()

	telem_process = multiprocessing.Process(target=receive_telem, args=(logger_queue, logger_worker_configurer, current_coordinates,))
	telem_process.start()

	obj_process = multiprocessing.Process(target=obj_receive, args=(logger_queue, logger_worker_configurer, current_obstacles,))
	obj_process.start()

	send_course_process = multiprocessing.Process(target=send_course, args=(logger_queue, logger_worker_configurer, guided_waypoint_input,))
	send_course_process.start()

	obstacle_map = ClientConverter(current_coordinates[0])
	is_obstacle_map_initialized = False

	waypoints = json.load(open(waypoint_JSON_file_path, 'r'))["items"]
	waypoints_list = []
	for json_waypoint in waypoints:
		waypoints_list.append(Waypoint(json_waypoint["coordinate"][0], json_waypoint["coordinate"][1], json_waypoint["coordinate"][2]))

	index = 0
	while True:
		if not is_obstacle_map_initialized and current_coordinates[0].get_latitude() != 0.0:
			obstacle_map = ClientConverter(current_coordinates[0])
			is_obstacle_map_initialized = True
		elif is_obstacle_map_initialized:
			if index == 50:
				print("Sending initial coordinates from main...")
				initial_coordinates = obstacle_map.getInitialCoordinates()
				guided_waypoint_output.send("lat " + str(initial_coordinates.get_latitude()) + " ")
				guided_waypoint_output.send("lng " + str(initial_coordinates.get_longitude()) + " ")
				guided_waypoint_output.send("alt " + str(initial_coordinates.get_altitude()) + " ")

			initialCoords = obstacle_map.getInitialCoordinates()
			haversine_distance = haversine(initialCoords.get_longitude(), initialCoords.get_latitude(), current_coordinates[0].get_longitude(), current_coordinates[0].get_latitude())
			updated_drone_location = ConverterDataUpdate(haversine_distance, current_coordinates[0].get_heading(), current_coordinates[0].get_altitude())
			obstacle_map.updateMainDroneMass(updated_drone_location)

			index += 1
			sleep(0.5)
