import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.bind(server_address)
sock.listen(1)
print("Waiting for a connection...")
connection, client_address = sock.accept()

while True:
    curr_coords = {
        "lat" : -1.0,
        "lng" : -1.0,
        "alt" : -1.0,
        "heading" : -1
    }

    while curr_coords["lat"] == -1.0 or curr_coords["lng"] == -1.0 or curr_coords["alt"] == -1.0 or curr_coords["heading"] == -1:
        print("Receiving data...")
        data = connection.recv(16)
        print >>sys.stderr, 'receied "%s"' % data

        messages = data.split(" ")
        for index in range(len(message) - 1):
            if "lat" in messages[index] or "lng" in messages[index] or "alt" in messages[index] or "heading" in messages[index]:
                curr_coords[messages[index]] = float(messages[index + 1])

    print("curr_coords FULL")
    print(curr_coords)
    sys.exit(0)
