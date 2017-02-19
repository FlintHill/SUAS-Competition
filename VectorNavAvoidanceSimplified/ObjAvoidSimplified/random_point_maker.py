'''
Created on Feb 17, 2017

@author: vtolpegin
'''
import numpy as np
import random

def get_random_points_in_bounds(dimensions, num_points, bounds):
    points = np.zeros(dimensions)
    for i in range(num_points):
        components = []
        for dim in range(dimensions):
            rand_value = random.randint(bounds[dim][0], bounds[dim][1])
            components.append(rand_value)
        points = np.vstack((points, np.array(components)))

    return points[1:]
