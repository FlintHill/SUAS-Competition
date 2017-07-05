from SUASSystem import Location
from SUASSystem import VehicleState
import math
import interop
import numpy

def get_location(vehicle):
    """
    Convert the vehicle's current location to a Location object

    :param vehicle: The vehicle to convert
    """
    latitude = vehicle.location.global_relative_frame.lat
    longitude = vehicle.location.global_relative_frame.lon
    altitude = vehicle.location.global_relative_frame.alt * 3.28084

    return Location(latitude, longitude, altitude)

def get_vehicle_state(vehicle, MSL_ALT):
    """
    Convert the vehicle's current position and information into a vehicle
    state object

    :param vehicle: The vehicle to convert
    :param sda_converter: The sda converter
    :type sda_converter: SDAConverter
    """
    latitude = vehicle.location.global_relative_frame.lat
    longitude = vehicle.location.global_relative_frame.lon
    altitude = (vehicle.location.global_relative_frame.alt * 3.28084) + MSL_ALT
    groundspeed = vehicle.groundspeed * 1.94384448
    velocity = vehicle.velocity
    direction = vehicle.heading

    return VehicleState(latitude, longitude, altitude, direction, groundspeed, velocity, False, vehicle.commands.next)

def get_obstacle_location(obstacle, MSL_ALT):
    """
    Get an Obstacle's location

    :param obstacle: The obstacle to convert
    :type obstacle: StationaryObstacle or MovingObstacle
    """
    latitude = obstacle.latitude
    longitude = obstacle.longitude
    if isinstance(obstacle, interop.StationaryObstacle):
        altitude = obstacle.cylinder_height
    else:
        altitude = obstacle.altitude_msl + obstacle.sphere_radius - MSL_ALT

    return Location(latitude, longitude, altitude)

def get_mission_json(mission, obstacles):
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
    mission_in_json["stationary_obstacles"] = [
        {
            "latitude" : stationary_obstacle.latitude,
            "longitude" : stationary_obstacle.longitude,
            "cylinder_radius" : stationary_obstacle.cylinder_radius,
            "cylinder_height" : stationary_obstacle.cylinder_height
        } for stationary_obstacle in obstacles[0]
    ]
    mission_in_json["moving_obstacles"] = [
        {
            "altitude_msl" : moving_obstacle.altitude_msl,
            "latitude" : moving_obstacle.latitude,
            "longitude" : moving_obstacle.longitude,
            "cylinder_radius" : moving_obstacle.sphere_radius
        } for moving_obstacle in obstacles[1]
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
    dx, dy, dz = haversine(initial_location, new_location, units="US")

    return numpy.array([dx, dy, new_location.get_alt()])

def haversine(location1, location2, units="METRIC"):
    """
    Calculates the great circle distance between two points
    on the earth (specified in decimal degrees)

    :param location1: The first GPS location
    :type location1: Location
    :param location2: The second GPS location
    :type location2: Location
    """
    dz = location2.get_alt() - location1.get_alt()
    dy = (location2.get_lat() - location1.get_lat()) * 69.172
    dx = (location2.get_lon() - location1.get_lon()) * 69.172 * math.cos(math.radians(location1.get_lat() + location2.get_lat()) / 2)

    if "metric" in units.lower():
        dy *= 1609.34
        dx *= 1609.34
    elif "us" in units.lower():
        dy *= 1609.34 * 3.28084
        dx *= 1609.34 * 3.28084

    return dx, dy, dz

def inverse_haversine(location1, point):
    """
    Calculate a second GPS point through using a single GPS point and a
    different in XY units

    :param location1: The first GPS coordinate
    :type location1: Location
    :param point: The point in the map that the obstacle occupies
    :type point: Numpy Array
    """
    dy = point[1] / (3.28084 * 1000)
    dx = point[0] / (3.28084 * 1000)

    lat = location1.get_lat() + (dy / 111.195)
    lon = location1.get_lon() + (dx / (math.cos(math.radians((lat + location1.get_lat()) / 2.0)) * 111.191))
    alt = point[2] / 3.28084

    return Location(lat, lon, alt)

def bearing(location1, location2):
    """
    Calculates the bearing between two points

    :param location1: The first GPS location
    :type location1: Location
    :param location2: The second GPS location
    :type location2: Location
    """
    dx, dy, dz = haversine(location1, location2)
    initial_bearing = math.atan2(dx, dy)

    return initial_bearing
