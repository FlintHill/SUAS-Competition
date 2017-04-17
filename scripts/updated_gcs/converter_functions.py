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

def get_mission_json(mission):
    """
    Convert a Mission object to a JSON format
    """
    mission_in_json = {}
    mission_in_json["air_drop_pos"] = {
        "latitude" : mission.air_drop_pos.latitude,
        "longitude" : mission.air_drop_pos.longitude
    }
    mission_in_json["fly_zones"] = [
        {"altitude_msl_min" : fly_zone.altitude_msl_min,
        "altitude_msl_max" : fly_zone.altitude_msl_max,
        "boundary_pts" : [
            {
                "latitude" : point.latitude,
                "longitude" : point.longitude,
                "order" : point.order
            } for point in fly_zone.boundary_pts
        ]} for fly_zone in mission.fly_zones
    ]
    mission_in_json["home_pos"] = {
        "latitude" : mission.home_pos.latitude,
        "longitude" : mission.home_pos.longitude
    }
    mission_in_json["mission_waypoints"] = [
        {
            "altitude_msl" : mission_waypoint.altitude_msl,
            "latitude" : mission_waypoint.latitude,
            "longitude" : mission_waypoint.longitude,
            "order" : mission_waypoint.order
        } for mission_waypoint in mission.mission_waypoints
    ]
    mission_in_json["off_axis_target_pos"] = {
        "latitude" : mission.off_axis_target_pos.latitude,
        "longitude" : mission.off_axis_target_pos.longitude
    }
    mission_in_json["emergent_last_known_pos"] = {
        "latitude" : mission.emergent_last_known_pos.latitude,
        "longitude" : mission.emergent_last_known_pos.longitude
    }
    mission_in_json["search_grid_points"] = [
        {
            "altitude_msl" : search_grid_point.altitude_msl,
            "latitude" : search_grid_point.latitude,
            "longitude" : search_grid_point.longitude,
            "order" : search_grid_point.order
        } for search_grid_point in mission.search_grid_points
    ]

    return mission_in_json

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
