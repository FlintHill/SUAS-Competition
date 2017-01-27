import socket
import multiprocessing
import sys
from math import radians, cos, sin, asin, sqrt
from time import sleep

INTEROP_CLIENT_ADDRESS = ('localhost', 9000)

class Message(object):
    """
    Simple container class to send messages through multiprocessing
    pipes
    """

    def __init__(self, message):
        """
        Initialize a Message object

        :param message: Message to send through the pipe
        """
        self.message = message

    def get_message(self):
        """
        Returns the message
        """
        return self.message

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def bearing(lon1, lat1, lon2, lat2):
    bearing = atan2(sin(lon2-lon1)*cos(lat2), cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(lon2-lon1))
    bearing = degrees(bearing)
    bearing = (bearing + 360) % 360

    return bearing

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

	while True:
		sleep(0.5)

def send_course(input_pipe):
    """
    Send course to mission planner instance

    :param output_pipe: The data to send to the mission planner instances
        goes through this pipe
	"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10001)
	is_connected = False
	while not is_connected:
		try:
			print("Connecting to send_course socket...")
			sock.connect(server_address)

			is_connected = True
		except:
			print("Socket for send_course is not open...")
			sleep(0.1)

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

    while True:
        curr_coords = {
            "lat" : -1.0,
            "lng" : -1.0,
            "alt" : -1.0,
            "heading" : -1
        }

        previous_message = None
        while curr_coords["lat"] == -1.0 or curr_coords["lng"] == -1.0 or curr_coords["alt"] == -1.0 or curr_coords["heading"] == -1:
            print("Receiving data...")
            data = connection.recv(64).decode("utf-8")
            print('received "%s"' % data)

            messages = data.split(" ")
            for index in range(len(messages) - 1):
                if previous_message:
                    curr_coords[previous_message] = float(messages[index])
                    previous_message = None
                elif messages[index] in curr_coords:
                    previous_message = messages[index]

        print(curr_coords)
        current_coordinates_array[0] = curr_coords["lat"]
        current_coordinates_array[1] = curr_coords["lng"]
        current_coordinates_array[2] = curr_coords["alt"]
        current_coordinates_array[3] = curr_coords["heading"]

if __name__ == '__main__':
    manager = multiprocessing.Manager()

    current_coordinates = manager.list()
    current_coordinates.extend([0.0, 0.0, 0.0, 0.0])
    current_obstacles = manager.list()

    guided_waypoint_input, guided_waypoint_output = multiprocessing.Pipe()

    telem_process = multiprocessing.Process(target=receive_telem, args=(current_coordinates,))
    telem_process.start()

    obj_process = multiprocessing.Process(target=obj_receive, args=(current_obstacles,))
    obj_process.start()

    send_course_process = multiprocessing.Process(target=send_course, args=(guided_waypoint_input,))
    send_course_process.start()

    while True:
        print(current_coordinates[0])
        print(current_obstacles[:])
        sleep(0.5)
