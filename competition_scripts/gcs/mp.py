from time import time
from time import sleep
from math import radians, cos, sin, asin, sqrt, pi
from datetime import datetime
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
    Calculates the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    dy = (lat2 - lat1) * 69.172 * 1609.34
    dx = (lon2 - lon1) * 69.172 * cos((lat1 + lat2) * pi / 360.0) * 1609.34

    dist = (dy**2 + dx**2)**0.5 * 0.999

    return dist

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
	alt_diff = abs(coords2[2] - coords1[2])

	print("diff: " + str(diff))
	print("alt_diff: " + str(alt_diff))
	print("coords1[2]: " + str(coords1[2]))
	print("coords2[2]: " + str(coords2[2]))

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
guided_coords = {
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

		if guided_coords["lat"] != -1.0 and guided_coords["lng"] != -1.0 and guided_coords["alt"] != -1.0 and (has_reached_waypoint([guided_coords["lat"], guided_coords["lng"], guided_coords["alt"]], [cs.lat, cs.lng, cs.alt])):
			Script.ChangeMode("Auto")
			current_flight_mode = "Auto"

			guided_coords = {
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
				MissionPlanner.Utilities.Locationwp.alt.SetValue(new_waypoint, float(data_coords["alt"] / 3.28084))
				MAV.setGuidedModeWP(new_waypoint)

				guided_coords = {
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
