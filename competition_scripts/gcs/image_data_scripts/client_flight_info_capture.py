import socket
import json
from datetime import datetime
from time import sleep
import pickle

SAVE_COORDINATES_PATH = "./location_mission_data.json"

def save_to_file(data, file_path):
    """
    Saves a set of data to a file
    """
    with open(file_path, 'w+') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)

def receive_telem():
	"""
	Receive telemetry from the local mission planner instance
	"""
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('localhost', 10000)
	sock.bind(server_address)
	sock.listen(1)
	connection, client_address = sock.accept()

    coordinates = {}
    try:
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

    		curr_coords["heading"] *= math.pi / 180.0
            coordinates[pickle.dumps(datetime.now())] = curr_coords
    		CurrentCoordinates(curr_coords["lat"], curr_coords["lng"], curr_coords["alt"], curr_coords["heading"])
    except:
        save_to_file(coordinates, SAVE_COORDINATES_PATH)

if __name__ == '__main__':
	receive_telem()
