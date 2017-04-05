from SDA import *
from converter_functions import *
from location_data import Location
import numpy

class SDAConverter(object):
    """
    Converts between geolocations and cartesian coordinates to use the SDA
    algorithm implemented
    """

    def __init__(self, initial_coordinates):
        """
        Initialize the converter

        :param initial_coordinates: The initial GPS coordinates of the UAV
        :type initial_coordinates: GPSCoordinates
        """
        self.obstacle_map = ObstacleMap()

        self.initial_coordinates = initial_coordinates
        self.previous_min_tangent_point = numpy.array([0, 0])
        self.minimum_change_in_guided_waypoint = 3

        # REMOVE THE BELOW LINE DURING ACTUAL FLIGHT
        #self.obstacle_map.add_obstacle(StationaryObstacle(numpy.array([100.0, -8.0]), 5));

    def set_waypoint(self, new_waypoint):
        """
        Set the current waypoint

        :param new_waypoint: The new waypoint
        :type new_waypoint: Location
        """
        converted_waypoint = convert_to_point(self.initial_coordinates, new_waypoint)

        self.obstacle_map.reset_waypoints()
        self.obstacle_map.add_waypoint(converted_waypoint)

    def add_obstacle(self, obstacle_location, obstacle):
        """
        Add an obstacle to the obstacle map

        :param obstacle_location: The obstacle's GPS location
        :type obstacle_location: Location
        :param obstacle: The obstacle to add
        :type obstacle: StationaryObstacle or MovingObstacle
        """
        converted_obstacle_location = convert_to_point(self.initial_coordinates, obstacle_location)
        new_obstacle = StationaryObstacle(converted_obstacle_location, 5)

        self.obstacle_map.add_obstacle(new_obstacle)

    def reset_obstacles(self):
        """
        Remove all obstacles currently on the obstacle map
        """
        self.obstacle_map.reset_obstacles()

    def set_uav_position(self, new_location):
        """
        Set the UAV's current position within the map

        :param new_location: The UAV's new location
        :type new_location: Location
        """
        converted_uav_location = convert_to_point(self.initial_coordinates, new_location)

        self.obstacle_map.set_drone_position(converted_uav_location)
        print(converted_uav_location)

    def avoid_obstacles(self, bearing):
        """
        Run obstacle avoidance using the drone's new position

        :param uav_bearing: The bearing of the UAV (in radians)
        :type uav_bearing: float
        """
        obstacle_in_path_boolean, avoid_coords = self.obstacle_map.is_obstacle_in_path()

        if obstacle_in_path_boolean:
            min_tangent_point = self.obstacle_map.get_min_tangent_point(avoid_coords)

            if VectorMath.get_magnitude(self.previous_min_tangent_point, min_tangent_point) > self.minimum_change_in_guided_waypoint:
                self.previous_min_tangent_point = min_tangent_point

                return inverse_haversine(self.initial_coordinates, min_tangent_point, bearing).as_global_relative_frame()

        return None

    def has_uav_reached_guided_waypoint(self):
        """
        Return True if the UAV has reached the current guided waypoint
        """
        distance = VectorMath.get_magnitude(self.previous_min_tangent_point, self.obstacle_map.get_drone().get_point())
        return distance < Constants.MAX_DISTANCE_TO_TARGET
