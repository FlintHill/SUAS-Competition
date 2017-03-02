from time import time
from time import sleep
from math import radians, cos, sin, asin, sqrt
import socket
import sys
import MissionPlanner
import clr
clr.AddReference("MissionPlanner.Utilities")

receive_address = 'localhost'
receive_port_min = 10010
server_address = ('localhost', 10000)

def send_data(connection, data):
	"""
	Send data through a socket

	:param connection: The socket to send data through
	:param data: The data to send over the socket
	"""
	connection.sendall(data)

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

def has_reached_waypoint(coords1, coords2, maximum_distance=5.0):
	"""
	A simple script to determine if the difference between two sets of
		coordinates and see if the difference is less than a maximum
		distance

	:param coords1: The first location which takes the form
		[lat, lng, alt]
	:param coords2: The second location which takes the form
		[lat, lng, alt]
	;param maximum_distance: The maximum distance beteween the two locations
	"""
	diff = haversine(coords1[1], coords1[0], coords2[1], coords2[0])
	alt_diff = coords2[2] - coords1[2]

	if diff < maximum_distance and alt_diff < maximum_distance:
		return True

	return False

def timing(rate):
	"""
	Timing Generator, creates delays to achieve the given loop frequency
	Args:
		rate: Rate in Hertz
	"""
	next_time = time()
	while True:
		next_time += 1.0 / rate
		delay = int((next_time - time()) * 1000)
		if delay > 0:
			Script.Sleep(delay)
		yield

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_address)
for port in range(receive_port_min, receive_port_min + 10):
	try:
		receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		receive_socket.bind((receive_address, port))
		receive_socket.listen(1)
		print("Waiting for a connection...")
		receive_connection, receive_connection_address = receive_socket.accept()
		receive_connection.settimeout(0.1)
		print("Connected")

		break
	except:
		print("Could not create socket on port " + str(port))

data_coords = {
	"lat" : -1.0,
	"lng" : -1.0,
	"alt" : -1.0
}
new_wp_coords = {
	"lat" : -1.0,
	"lng" : -1.0,
	"alt" : -1.0
}
current_flight_mode = "Auto"
previous_message = None

while True:
	for _ in timing(rate=2):
		send_data(sock, "lat " + str(cs.lat) + " ")
		send_data(sock, "lng " + str(cs.lng) + " ")
		send_data(sock, "alt " + str(cs.alt) + " ")
		send_data(sock, "heading " + str(cs.groundcourse) + " ")

		if new_wp_coords["lat"] != -1.0 and new_wp_coords["lng"] != -1.0 and new_wp_coords["alt"] != -1.0 and has_reached_waypoint([new_wp_coords["lat"], new_wp_coords["lng"], new_wp_coords["alt"]], [cs.lat, cs.lng, cs.alt]):
			Script.ChangeMode("Auto")
			current_flight_mode = "Auto"

			new_wp_coords = {
				"lat" : -1.0,
				"lng" : -1.0,
				"alt" : -1.0
			}

			print("Completed movement, switched back into Auto")

		try:
			data = receive_connection.recv(64).decode("utf-8")

			messages = data.split(" ")
			for index in range(len(messages) - 1):
				if previous_message:
					data_coords[previous_message] = float(messages[index])
					previous_message = None
				elif messages[index] in data_coords:
					previous_message = messages[index]

			if data_coords["lat"] != -1.0 and data_coords["lng"] != -1.0 and data_coords["alt"] != -1.0:
				print("Avoiding an object...")

				if "Auto" in current_flight_mode:
					Script.ChangeMode("Guided")
					currrent_flight_mode = "Guided"

				new_waypoint = MissionPlanner.Utilities.Locationwp()
				MissionPlanner.Utilities.Locationwp.lat.SetValue(new_waypoint, float(data_coords["lat"]))
				MissionPlanner.Utilities.Locationwp.lng.SetValue(new_waypoint, float(data_coords["lng"]))
				MissionPlanner.Utilities.Locationwp.alt.SetValue(new_waypoint, float(data_coords["alt"]))
				MAV.setGuidedModeWP(new_waypoint)

				new_wp_coords = {
					"lat" : data_coords["lat"],
					"lng" : data_coords["lng"],
					"alt" : data_coords["alt"]
				}
				data_coords = {
					"lat" : -1.0,
					"lng" : -1.0,
					"alt" : -1.0
				}
		except socket.timeout:
			pass
