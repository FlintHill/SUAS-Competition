import os
from PIL import Image
import socket
import pickle
import struct

CROPS_DIR_LOCATION = "/media/SSD/crops/"
FULL_IMAGES_DIR_LOCATION = "/media/SSD/full_images/"
PORT = 9001

def load_crops():
    """
    Load all crops & associated data
    """
    crops = {}

    files = [f for f in listdir(CROPS_DIR_LOCATION) if ".png" in f)]
    for file_name in files:
        crop_number = file_name[ : file_name.find(".")]
        crops[crop_number]["crop"] = Image.open(os.path.join(CROPS_DIR_LOCATION, file_name))

        crop_data_file_name = os.path.join(CROPS_DIR_LOCATION, crop_number + ".txt")
        with open(crop_data_file_name) as data_file:
            lines = crop_data_file.read().split()
            for line in lines:
                line_data = line.split(":")
                crops[crop_number]["info"][str(line_data[0])] = float(line_data[1])

    return crops

def encode_data(data):
    """
    Encode data into a transmittable message.

    @returns the encoded data
    """
    msg = pickle.dumps(data)
    msg = struct.pack('>I', len(msg)) + msg

    return msg

def create_listen_socket(port, max_connections):
    """
    Create a socket to listen on a port with max_connections.
    """
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(('', port))
    listen_socket.listen(max_connections)

    return listen_socket

if __name__ == '__main__':
    comm_socket = create_listen_socket(PORT, 1)
    connection, addr = comm_socket.accept()

    completed_crops = []

    #try:
    while True:
        # load Harrison's images
        crops = load_crops()

        # send them to Peter's image processing script
        # TODO : Add call to Peter's image processing script here
        for crop in crops:
            # We do not want to submit the same crop to the processor multiple
            #   times...
            if int(crop) not in completed_crops:
                is_crop, generated_crop_data = RunPetersCode(crops[crop]["crop"])

                if is_crop:
                    crops[crop]["target_attributes"] = generated_crop_data

                    # transmit the images and their information to the groundstation
                    connection.send(encode_data(crops[crop]))

    #except:
    #    comm_socket.close()
