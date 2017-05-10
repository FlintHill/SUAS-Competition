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
        self.current_path = numpy.array([])
        self.minimum_change_in_guided_waypoint = 3

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
        new_obstacle = StationaryObstacle(converted_obstacle_location, 100, 100)

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
        print("Current UAV position:", converted_uav_location)

    def avoid_obstacles(self):
        """
        Run obstacle avoidance using the drone's new position
        """
        obstacle_in_path_boolean, paths = self.obstacle_map.is_obstacle_in_path()

        if obstacle_in_path_boolean:
            min_path = self.obstacle_map.get_min_path(paths)

            if self.current_path.shape[0] == 0:
                self.current_path = min_path
            elif self.has_path_changed(self.current_path, min_path):
                self.current_path = min_path

    def has_path_changed(self, path1, path2):
        """
        Compares two paths to see if one has any changed points

        :param path1: The first path to compare
        :type path1: Numpy Array
        :param path2: The second path to compare
        :type path2: Numpy Array
        """
        if path1.shape[0] != path2.shape[0]:
            return True

        for index in range(path1.shape[0]):
            if VectorMath.get_magnitude(path1[index], path2[index]) > self.minimum_change_in_guided_waypoint:
                return True

        return False

    def get_uav_avoid_coordinates(self):
        """
        Return the coordinates to avoid the object
        """
        gps_points = []
        for xy_loc_point in self.current_path:
            gps_points.append(inverse_haversine(self.initial_coordinates, xy_loc_point).as_global_relative_frame())

        return gps_points

    def has_uav_reached_guided_waypoint(self):
        """
        Return True if the UAV has reached the current guided waypoint
        """
        if self.current_path.shape[0] != 0:
            distance = VectorMath.get_magnitude(self.current_path[0], self.obstacle_map.get_drone().get_point())

            if distance < Constants.MAX_DISTANCE_TO_TARGET:
                self.current_path = self.current_path[1:]

            print(self.current_path)

            return distance < Constants.MAX_DISTANCE_TO_TARGET

    def is_obstacle_in_path(self):
        """
        Return whether obstacle is in path of UAV
        """
        obstacle_in_path_boolean, avoid_coords = self.obstacle_map.is_obstacle_in_path()

        return obstacle_in_path_boolean
