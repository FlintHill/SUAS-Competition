import numpy
from math import acos, atan2, pi

def get_angle_between_vectors(v1, v2):
    return acos(numpy.dot(v1, v2)/(numpy.linalg.norm(v1) * numpy.linalg.norm(v2)))

def get_angle_of_2d_vector(vector):
    angle = atan2(vector[1], vector[0])
    if angle < 0:
        angle += 2*pi
    return angle