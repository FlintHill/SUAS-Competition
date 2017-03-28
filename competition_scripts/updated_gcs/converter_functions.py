from location_data import Location
from math_functions import *
import numpy

def get_location(vehicle):
    """
    Convert the vehicle's current location to a Location object

    :param vehicle: The vehicle to convert
    """
    latitude = vehicle.global_relative_frame.lat
    longitude = vehicle.global_relative_frame.lon
    altitude = vehicle.global_relative_frame.alt

    return Location(latitude, longitude, altitude)

def get_obstacle_location(obstacle):
    """
    Get an Obstacle's location

    :param obstacle: The obstacle to convert
    :type obstacle: StationaryObstacle or MovingObstacle
    """
    latitude = obstacle.latitude
    longitude = obstacle.longitude
    altitude = obstacle.altitude

    return Location(latitude, longitude, altitude)

def convert_to_point(initial_location, new_location):
    """
    Convert a location into a cartesian plane coordinate

    :param initial_location: The initial GPS location
    :type initial_location: Location
    :param new_location: The new location to convert to a cartesian point, based
        on (0,0) being at the initial location
    :type new_location: Location
    """
    haversine_dist = haversine(initial_location, new_location)
    obstacle_bearing = bearing(initial_location, new_location)

    dx = haversine_dist * cos(obstacle_bearing)
    dy = haversine_dist * sin(obstacle_bearing)

    return numpy.array([dx, dy])
