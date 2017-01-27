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

def receive_location(connection):
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

        if data == "NO DATA":
            return curr_coords

        messages = data.split(" ")
        for index in range(len(messages) - 1):
            if previous_message:
                curr_coords[previous_message] = float(messages[index])
                previous_message = None
            elif messages[index] in curr_coords:
                previous_message = messages[index]

    return curr_coords

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.connect(server_address)

receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receive_address = ('localhost', 10001)
receive_socket.bind(receive_address)
receive_socket.listen(1)
print("Waiting for a connection...")
receive_connection, receive_connection_address = receive_socket.accept()

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

        new_coords = receive_location(receive_connection)
        print(new_coords)
