import numpy
import os

def save_array(arr, path, name):
    if not os.path.exists(path):
        os.makedirs(path)
    numpy.save(path + "/" + name, arr)