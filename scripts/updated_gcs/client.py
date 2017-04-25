from dronekit import connect, VehicleMode
import socket
import multiprocessing
import pickle
import struct
from logger import *
from time import sleep
from interop_client import InteropClientConverter
from sda_converter import SDAConverter
from converter_functions import *
from sda_viewer import SDAViewSocket
from SimpleWebSocketServer import SimpleWebSocketServer
from vehicle_state import VehicleState
from SDA import *

TK1_ADDRESS = ('192.168.1.6', 9001)

UAV_CONNECTION_STRING = "tcp:127.0.0.1:5760"

INTEROP_URL = "http://10.10.130.100:8000"
INTEROP_USERNAME = "Flint"
INTEROP_PASSWORD = "2429875295"

MSL = 430
MIN_REL_FLYING_ALT = 100
MAX_REL_FLYING_ALT = 750

def read_data(connection):
    """
    Read a data from a socket.

    @returns the data received from the socket
    """
    raw_msglen = connection.recv(4)
    msglen = struct.unpack('>I', raw_msglen)[0]

    data = connection.recv(msglen)
    data = pickle.loads(data)

    return data

def sda_viewer_process(logger_queue, configurer, vehicle_state_data, mission_data):
    """
    Creates a process for the SDA viewer

    :param vehicle_state_process: The vehicle's current state
    :type vehicle_state_process: multiprocessing.Array
    """
    configurer(logger_queue)
    name = multiprocessing.current_process().name

    log(name, "Instantiating SDA Viewer process")
    sda_viewer_server = SimpleWebSocketServer('', 8000, SDAViewSocket, vehicle_state_data, mission_data)
    sda_viewer_server.serveforever()
    log(name, "SDA Viewer process instantiated")

def target_listener(logger_queue, configurer, received_targets_array):
    """
    Listen for targets sent from the TK1
    """
    configurer(logger_queue)
    name = multiprocessing.current_process().name

    tk1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    log(name, "Waiting to connect to the TK1...")
    tk1_socket.connect(TK1_ADDRESS)
    log(name, "Connected to TK1")

    while True:
        data = read_data(tk1_socket)

        print(data)

if __name__ == '__main__':
    interop_server_client = InteropClientConverter(MSL, INTEROP_URL, INTEROP_USERNAME, INTEROP_PASSWORD)

    logger_queue = multiprocessing.Queue(-1)
    logger_listener_process = multiprocessing.Process(target=listener_process, args=(logger_queue, logger_listener_configurer))
    logger_listener_process.start()

    manager = multiprocessing.Manager()
    received_targets = manager.list()
    # target_listener_process = multiprocessing.Process(target=target_listener, args=(logger_queue, logger_worker_configurer, received_targets))
    # target_listener_process.start()

    vehicle_state_data = manager.list()
    mission_data = manager.list()
    sda_viewer_process = multiprocessing.Process(target=sda_viewer_process, args=(logger_queue, logger_worker_configurer, vehicle_state_data, mission_data))
    sda_viewer_process.start()

    logger_worker_configurer(logger_queue)
    name = multiprocessing.current_process().name

    log(name, "Connecting to UAV on: %s" % UAV_CONNECTION_STRING)
    vehicle = connect(UAV_CONNECTION_STRING, wait_ready=True)
    vehicle.wait_ready('autopilot_version')
    log(name, "Connected to UAV on: %s" % UAV_CONNECTION_STRING)
    log_vehicle_state(vehicle, name)

    log(name, "Waiting for UAV to be armable")
    log(name, "Waiting for UAV to load waypoints")
    while len(vehicle.commands) < 1 and not vehicle.is_armable:
        sleep(0.05)

    log(name, "Downloading waypoints from UAV on: %s" % UAV_CONNECTION_STRING)
    waypoints = vehicle.commands
    waypoints.download()
    waypoints.wait_ready()
    log(name, "Waypoints successfully downloaded")

    log(name, "Enabling SDA...")
    sda_converter = SDAConverter(get_location(vehicle))
    sda_converter.set_waypoint(Location(38.8703041, -77.3214035, 100))
    #sda_converter.set_waypoint(Location(waypoints[0].x, waypoints[0].y, waypoints[0].z))
    log(name, "SDA enabled")
    vehicle_state_data.append(get_vehicle_state(vehicle, sda_converter))
    stationary_obstacles, moving_obstacles = interop_server_client.get_obstacles()
    obstacles_array = [stationary_obstacles, moving_obstacles]
    mission_data.append(get_mission_json(interop_server_client.get_active_mission(), obstacles_array))

    log(name, "Everything is instantiated...Beginning operation")
    #try:
    while True:
        """current_location = get_location(vehicle)
        current_waypoint_number = vehicle.commands.next
        current_uav_waypoint = waypoints[current_waypoint_number]
        sda_converter.set_waypoint(Location(current_uav_waypoint.x, current_uav_waypoint.y, current_uav_waypoint.z))

        interop_server_client.post_telemetry(current_location)"""
        stationary_obstacles, moving_obstacles = interop_server_client.get_obstacles()
        obstacles_array = [stationary_obstacles, moving_obstacles]
        """sda_converter.reset_obstacles()
        for stationary_obstacle in stationary_obstacles:
            sda_converter.add_obstacle(get_obstacle_location(stationary_obstacle), stationary_obstacle)
        for moving_obstacle in moving_obstacles:
            sda_converter.add_obstacle(get_obstacle_location(moving_obstacle), moving_obstacle)"""

        vehicle_state_data[0] = get_vehicle_state(vehicle, sda_converter)
        mission_data[0] = get_mission_json(interop_server_client.get_active_mission(), obstacles_array)

        sleep(0.5)
        """if vehicle.mode.name == "GUIDED" and sda_converter.has_uav_reached_guided_waypoint():
            vehicle.mode = VehicleMode("AUTO")

        sda_converter.set_uav_position(current_location)

        obj_avoid_coordinates = sda_converter.avoid_obstacles(math.radians(vehicle.heading) / 2)
        print(current_location.get_altitude())
        if obj_avoid_coordinates:
            log("root", "Avoiding obstacles...")
            vehicle.simple_goto(obj_avoid_coordinates)"""
    #except:
    #    pass#vehicle.close()
