from location_data import Location
from vehicle_state import VehicleState
from math_functions import *
import math
import numpy

def get_location(vehicle):
    """
    Convert the vehicle's current location to a Location object

    :param vehicle: The vehicle to convert
    """
    latitude = vehicle.location.global_relative_frame.lat
    longitude = vehicle.location.global_relative_frame.lon
    altitude = vehicle.location.global_relative_frame.alt

    return Location(latitude, longitude, altitude)

def get_vehicle_state(vehicle, sda_converter):
    """
    Convert the vehicle's current position and information into a vehicle
    state object

    :param vehicle: The vehicle to convert
    :param sda_converter: The sda converter
    :type sda_converter: SDAConverter
    """
    latitude = vehicle.location.global_relative_frame.lat
    longitude = vehicle.location.global_relative_frame.lon
    altitude = vehicle.location.global_relative_frame.alt
    groundspeed = vehicle.groundspeed
    velocity = vehicle.velocity
    direction = vehicle.heading

    return VehicleState(latitude, longitude, altitude, direction, groundspeed, velocity, sda_converter.is_obstacle_in_path())

def get_obstacle_location(obstacle):
    """
    Get an Obstacle's location

    :param obstacle: The obstacle to convert
    :type obstacle: StationaryObstacle or MovingObstacle
    """
    latitude = obstacle.latitude
    longitude = obstacle.longitude
    altitude = 0#obstacle.altitude

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

    dx = haversine_dist * math.cos(obstacle_bearing)
    dy = haversine_dist * math.sin(obstacle_bearing)

    return numpy.array([dx, dy])
