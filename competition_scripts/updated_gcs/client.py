from dronekit import connect, VehicleMode
import socket
import multiprocessing
from logger import *
from time import sleep
from interop_client import InteropClientConverter
from sda_converter import SDAConverter
from converter_functions import *
from SDA import *

TK1_ADDRESS = ('IP', 9001)

UAV_CONNECTION_STRING = "127.0.0.1:14550"

INTEROP_URL = "http://10.10.130.2:8000"
INTEROP_USERNAME = "Flint"
INTEROP_PASSWORD = "2429875295"

MSL = 430
MIN_REL_FLYING_ALT = 100
MAX_REL_FLYING_ALT = 750

def target_listener(logger_queue, configurer, received_targets_array):
	"""
	Listen for targets sent from the TK1
	"""
    configurer(logger_queue)
	name = multiprocessing.current_process().name

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#sock.bind(TK1_ADDRESS)
	#sock.listen(1)
	log(name, "Waiting for a connection to the TK1...")
	#connection, client_address = sock.accept()
	log(name, "Connected to TK1")

	while True:
		sleep(0.5)

if __name__ == '__main__':
	#interop_server_client = InteropClientConverter(MSL, INTEROP_URL, INTEROP_USERNAME, INTEROP_PASSWORD)

	logger_queue = multiprocessing.Queue(-1)
	logger_listener_process = multiprocessing.Process(target=listener_process, args=(logger_queue, logger_listener_configurer))
	logger_listener_process.start()

    manager = multiprocessing.Manager()
    received_targets = manager.list()
    # target_listener_process = multiprocessing.Process(target=target_listener, args=(logger_queue, logger_listener_configurer, received_targets))
    # target_listener_process.start()

    logger_listener_configurer(configurer)
    name = multiprocessing.current_process().name

    log(name, "Connecting to UAV on: %s" % UAV_CONNECTION_STRING)
    vehicle = connect(UAV_CONNECTION_STRING, wait_ready=True)
    vehicle.wait_ready('autopilot_version')
    log(name, "Connected to UAV on: %s" % UAV_CONNECTION_STRING)
    log_vehicle_state(vehicle, name)

	log(name, "Downloading waypoints from UAV on: %s" % UAV_CONNECTION_STRING)
    waypoints = vehicle.commands
    waypoints.download()
    waypoints.wait_ready()
    log(name, "Waypoints successfully downloaded")

    log(name, "Waiting for UAV to be armable")
	while not vehicle.is_armable:
        sleep(0.05)
    log(name, "Enabling SDA...")
    sda_converter = SDAConverter(get_location(vehicle))
    sda_converter.set_waypoints(waypoints)

    try:
    	while True:
            current_location = get_location(vehicle)

    		#interop_server_client.post_telemetry(current_location)
    		#stationary_obstacles, moving_obstacles = interop_server_client.get_obstacles()
    		#obstacle_map.reset_obstacles()
    		#for stationary_obstacle in stationary_obstacles:
    		#	obstacle_map.add_obstacle(get_obstacle_location(stationary_obstacle), stationary_obstacle)
            #for moving_obstacle in moving_obstacles:
            #   obstacle_map.add_obstacle(get_obstacle_location(moving_obstacle), moving_obstacle)

            if vehicle.mode.name == "GUIDED" and sda_converter.has_uav_reached_guided_waypoint():
                vehicle.mode = VehicleMode("AUTO")

            sda_converter.set_uav_position(current_location)

            obj_avoid_coordinates = sda_converter.avoid_obstacles()
    		if obj_avoid_coordinates:
    			log("root", "Avoiding obstacles...")
                vehicle.simple_goto(obj_avoid_coordinates)
    except:
        vehicle.close()
