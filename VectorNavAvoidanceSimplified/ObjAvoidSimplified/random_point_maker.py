'''
Created on Feb 17, 2017

@author: vtolpegin
'''

import random

def get_random_point_in_bounds(dimensions, numPoints, bounds):
    points = []
    for i in range(0, numPoints):
        components = []
        for dim in range(0, dimensions):
            randComp = random.randint(bounds[dim][0], bounds[dim][1])
            components.append(randComp)
        points.append(MultiDimPoint(components))
    return points
