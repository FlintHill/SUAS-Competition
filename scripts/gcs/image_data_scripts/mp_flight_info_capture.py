from time import time
from time import sleep
import socket
import MissionPlanner
import clr
clr.AddReference("MissionPlanner.Utilities")

server_address = ('localhost', 10000)

def send_data(connection, data):
	"""
	Send data through a socket

	:param connection: The socket to send data through
	:param data: The data to send over the socket
	"""
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

while True:
	for _ in timing(rate=5):
		send_data(sock, "lat " + str(cs.lat) + " ")
		send_data(sock, "lng " + str(cs.lng) + " ")
		send_data(sock, "alt " + str(cs.alt) + " ")
		send_data(sock, "heading " + str(cs.groundcourse) + " ")
