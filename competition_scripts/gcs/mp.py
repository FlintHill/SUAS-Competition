from time import time
import socket
import sys

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
server_address = ('localhost', 10000)
sock.connect(server_address)

while True:
    for _ in timing(rate=2):
        print(cs.lat)
        print(cs.lng)
        print(cs.alt)
        print(cs.groundcourse)

        send_data(sock, "lat " + str(cs.lat) + " ")
        send_data(sock, "lng " + str(cs.lng) + " ")
        send_data(sock, "alt " + str(cs.alt) + " ")
        send_data(sock, "heading " + str(cs.groundcourse) + " ")
