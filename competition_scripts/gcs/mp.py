from time import time
from time import sleep
import socket
import sys
import MissionPlanner
import clr
clr.AddReference("MissionPlanner.Utilities")

receive_address = 'localhost'
server_address = ('localhost', 10000)

def send_data(connection, data):
	connection.sendall(data)

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

port_min = 10001
for port in range(port_min, port_min + 10):
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

curr_coords = {
	"lat" : -1.0,
	"lng" : -1.0,
	"alt" : -1.0
}

previous_message = None
while True:
	for _ in timing(rate=2):
		send_data(sock, "lat " + str(cs.lat) + " ")
		send_data(sock, "lng " + str(cs.lng) + " ")
		send_data(sock, "alt " + str(cs.alt) + " ")
		send_data(sock, "heading " + str(cs.groundcourse) + " ")

		try:
			data = receive_connection.recv(64).decode("utf-8")

			messages = data.split(" ")
			for index in range(len(messages) - 1):
				if previous_message:
					curr_coords[previous_message] = float(messages[index])
					previous_message = None
				elif messages[index] in curr_coords:
					previous_message = messages[index]

			if curr_coords["lat"] != -1.0 and curr_coords["lng"] != -1.0 and curr_coords["alt"] != -1.0:
				print("Avoiding an object...")

				Script.ChangeMode("Guided")
				new_waypoint = MissionPlanner.Utilities.Locationwp()
				MissionPlanner.Utilities.Locationwp.lat.SetValue(new_waypoint, float(curr_coords["lat"]))
				MissionPlanner.Utilities.Locationwp.lng.SetValue(new_waypoint, float(curr_coords["lng"]))
				MissionPlanner.Utilities.Locationwp.alt.SetValue(new_waypoint, float(curr_coords["alt"]))
				MAV.setGuidedModeWP(new_waypoint)
				#Script.ChangeMode("Auto")

				curr_coords = {
					"lat" : -1.0,
					"lng" : -1.0,
					"alt" : -1.0
				}
		except socket.timeout:
			pass
