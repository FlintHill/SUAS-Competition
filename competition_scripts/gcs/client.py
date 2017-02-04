import socket
import multiprocessing
import sys
import json
from time import sleep
from static_math import haversine, bearing
from current_coordinates import CurrentCoordinates
from converter_data_update import ConverterDataUpdate
from ClientConverter import ClientConverter
from obstacle import Obstacle
from message import Message

INTEROP_CLIENT_ADDRESS = ('localhost', 9000)
server_address = ('localhost', 10001)
waypoint_JSON_file_path = "./data/demo_waypoints.mission"

def send_data(connection, data):
	connection.sendall(data)

def obj_receive(object_array):
    """
    Receive obstacles from the interoperability server

    :param object_array: The multiprocessing list to use to store obstacles
        from interop server
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(INTEROP_CLIENT_ADDRESS)
    sock.listen(1)
    print("Waiting for a connection to INTEROP_CLIENT...")
    connection, client_address = sock.accept()
    print("Connected to INTEROP_CLIENT")

    while True:
        sleep(0.5)

def send_course(input_pipe):
    """
    Send course to mission planner instance

    :param output_pipe: The data to send to the mission planner instances
        goes through this pipe
	"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    is_connected = False
    while not is_connected:
        try:
            print("Connecting to send_course socket...")
            sock.connect(server_address)

            is_connected = True
        except:
            print("Socket for send_course is not open...")
            sleep(0.1)
    print("Connected to send_course socket")

    while True:
        if input_pipe.poll():
            data = input_pipe.recv()

            send_data(sock, data)
        else:
            send_data(sock, "------------NO DATA------------")

        sleep(0.05)

def receive_telem(current_coordinates_array):
    """
    Receive telemetry from the local mission planner instance

    :param current_coordinates_array: The multiprocessing list to use to
        store received telem data from mission planner
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10000)
    sock.bind(server_address)
    sock.listen(1)
    print("Waiting for a connection to MP...")
    connection, client_address = sock.accept()
    print("Connected to MP")

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

        current_coordinates_array[0] = CurrentCoordinates(curr_coords["lat"], curr_coords["lng"], curr_coords["alt"], curr_coords["heading"])

if __name__ == '__main__':
    manager = multiprocessing.Manager()

    current_coordinates = manager.list()
    current_coordinates.extend([CurrentCoordinates(0.0, 0.0, 0.0, 0.0)])
    current_obstacles = manager.list()

    guided_waypoint_input, guided_waypoint_output = multiprocessing.Pipe()

    telem_process = multiprocessing.Process(target=receive_telem, args=(current_coordinates,))
    telem_process.start()

    obj_process = multiprocessing.Process(target=obj_receive, args=(current_obstacles,))
    obj_process.start()

    send_course_process = multiprocessing.Process(target=send_course, args=(guided_waypoint_input,))
    send_course_process.start()

    obstacle_map = ClientConverter(current_coordinates[0])
    is_obstacle_map_initialized = False

    waypoints = json.load(open(waypoint_JSON_file_path, 'r'))

    while True:
        if not is_obstacle_map_initialized and current_coordinates[0].get_latitude() != 0.0:
            obstacle_map = ClientConverter(current_coordinates[0])
            is_obstacle_map_initialized = True
        elif is_obstacle_map_initialized:
            print("Updating obstacle map...")

            initialCoords = obstacle_map.getInitialCoordinates()
            haversine_distance = haversine(initialCoords.get_latitude(), initialCoords.get_longitude(), current_coordinates[0].get_latitude(), current_coordinates[0].get_longitude())
            updated_drone_location = ConverterDataUpdate(haversine_distance, current_coordinates[0].get_heading(), current_coordinates[0].get_altitude())
            obstacle_map.updateMainDroneMass(updated_drone_location)

            sleep(0.5)
