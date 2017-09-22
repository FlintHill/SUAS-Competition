from SDA import *
from SUASSystem import *
import numpy
import interop

class SDAConverter(object):
    """
    Converts between geolocations and cartesian coordinates to use the SDA
    algorithm implemented
    """

    def __init__(self, initial_coordinates, fly_zones):
        """
        Initialize the converter

        :param initial_coordinates: The initial GPS coordinates of the UAV
        :type initial_coordinates: Location
        :param fly_zones: The fly zones where the UAV can be
        :type fly_zones: Numpy Array
        """
        self.initial_coordinates = initial_coordinates
        self.current_path = numpy.array([])
        self.current_path_index = 1
        self.minimum_change_in_guided_waypoint = 3

        converted_boundary_points = self.convert_fly_zones(numpy.array([fly_zones]))
        self.obstacle_map = ObstacleMap(numpy.array([0,0,0]), converted_boundary_points)

    def convert_fly_zones(self, fly_zones):
        """
        Wrapper method for converting a list of fly zones
        """
        converted_fly_zones = []
        for fly_zone in fly_zones:
            converted_fly_zones.append(self.convert_fly_zone(fly_zone))

        return numpy.array(converted_fly_zones)

    def convert_fly_zone(self, fly_zone):
        """
        Converts a bunch of boundary points to the XY coordinate mapping

        :param fly_zone: The boundary points that need to be converted
        :type fly_zone: List (of Location objects)
        """
        converted_boundary_points = []
        for index in range(len(fly_zone)):
            for boundary_point in fly_zone[index]["boundary_pts"]:
                if boundary_point["order"] == index:
                    boundary_point_geo = Location(boundary_point["latitude"], boundary_point["longitude"], 0)
                    converted_boundary_points.append(convert_to_point(self.initial_coordinates, boundary_point_geo)[:2])
                    break

        return numpy.array(converted_boundary_points)

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
        :type obstacle: StationaryObstacle
        """
        converted_obstacle_location = convert_to_point(self.initial_coordinates, obstacle_location)

        new_obstacle = StationaryObstacle(converted_obstacle_location, obstacle.cylinder_radius, obstacle.cylinder_height)

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

        if not self.has_uav_completed_guided_path():
            if self.get_distance_to_current_guided_waypoint() < Constants.MAX_DISTANCE_TO_TARGET:
                self.current_path_index += 1

        print("Current UAV position:", converted_uav_location)

    def avoid_obstacles(self):
        """
        Run obstacle avoidance using the drone's new position
        """
        obstacle_in_path_boolean, paths = self.obstacle_map.is_obstacle_in_path()

        print("Obstacle in path:", obstacle_in_path_boolean)
        if obstacle_in_path_boolean:
            min_path = self.obstacle_map.get_min_path(paths)

            if self.current_path.shape[0] == 0:
                self.current_path_index = 0
                self.current_path = min_path
            elif self.has_path_changed(self.current_path, min_path):
                self.current_path_index = 0
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

    def has_uav_completed_guided_path(self):
        """
        Returns True if the UAV has completed the guided path, False if not
        """
        return self.current_path_index >= len(self.current_path)

    def does_guided_path_exist(self):
        """
        Returns True if a guided path exists and False otherwise
        """
        return self.current_path.shape[0] != 0

    def get_uav_avoid_coordinates(self):
        """
        Return the current coordinates to avoid the object
        """
        gps_points = []
        for xy_loc_point in self.current_path:
            gps_points.append(inverse_haversine(self.initial_coordinates, xy_loc_point))

        return gps_points[self.current_path_index]

    def has_uav_reached_guided_waypoint(self):
        """
        Return True if the UAV has reached the current guided waypoint
        """
        return self.get_distance_to_current_guided_waypoint() < Constants.MAX_DISTANCE_TO_TARGET

    def get_distance_to_current_guided_waypoint(self):
        """
        Returns the distance to the current guided waypoint
        """
        if does_guided_path_exist:
            distance = VectorMath.get_magnitude(self.current_path[self.current_path_index], self.obstacle_map.get_drone().get_point())

            return distance

        # Any really high number will work here
        return 100000000

    def is_obstacle_in_path(self):
        """
        Return whether obstacle is in path of UAV
        """
        obstacle_in_path_boolean, avoid_coords = self.obstacle_map.is_obstacle_in_path()

        return obstacle_in_path_boolean
