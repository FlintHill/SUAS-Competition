import os
from PIL import Image
import socket
import pickle
import struct

CROPS_DIR_LOCATION = "/media/SSD/crops/"
FULL_IMAGES_DIR_LOCATION = "/media/SSD/full_images/"
PORT = 9001

def load_images_from_dir(dir):
    """
    Load all images in a directory and their associated information files
    """
    images = []

    files = [f for f in listdir(mypath) if isfile(os.join(mypath, f))]
    for file_name in files:
        images.append(Image.open(file_name))

    for file_name in files:
        os.remove(file_name)

    return images

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

    #try:
    while True:
        # load Harrison's images
        crops = load_images_from_dir(CROPS_DIR_LOCATION)

        # send them to Peter's image processing script
        # TODO : Add call to Peter's image processing script here
        data = {}
        data["target_attributes"] = {}

        # transmit the images and their information to the groundstation
        connection.send(encode_data(task))

    #except:
    #    comm_socket.close()
