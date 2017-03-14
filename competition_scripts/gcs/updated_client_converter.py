from SDA import *
from current_coordinates import CurrentCoordinates
from math import sin, cos, atan2
from static_math import *
import numpy as np

class ClientConverter(object):
    """
    Converts between geolocations and cartesian coordinates to use the SDA
    algorithm implemented
    """

    def __init__(self, initial_coordinates):
        self.obstacle_map = ObstacleMap()

        self.initial_coordinates = initial_coordinates
        self.previous_min_tangent_point = np.array([0, 0])
        self.minimum_change_in_guided_point = 1

        self.obstacle_map.add_obstacle(StationaryObstacle(np.array([100, 10]), 5));

    def get_initial_coordinates(self):
        return self.initial_coordinates

    def set_waypoints(self, new_waypoints):
        for waypoint in new_waypoints:
            converted_waypoint = np.array(waypoint.convert_to_point(self.get_initial_coordinates())[:-1])

            self.obstacle_map.add_waypoint(converted_waypoint)

    def add_obstacle(self, obstacle):
        """
        Add an obstacle to the obstacle map

        :param obstacle: The obstacle to add
        :type obstacle: StationaryObstacle or MovingObstacle
        """
        initial_coordinates = self.get_initial_coordinates()
        haversine_dist = haversine(initial_coordinates, GPSCoordinates(obstacle.latitude, obstacle.longitude, initial_coordinates.get_altitude()))
        obstacle_bearing = bearing(initial_coordinates, GPSCoordinates(obstacle.latitude, obstacle.longitude, initial_coordinates.get_altitude()))

        dx = haversine_dist * cos(obstacle_bearing)
        dy = haversine_dist * sin(obstacle_bearing)
        new_mass_obstacle = np.array([StationaryObstacle(np.array([dx, dy]), 5)])

        self.obstacle_map.add_obstacle(new_mass_obstacle)

    def update_drone_mass_position(self, update_data):
        """
        Run obstacle avoidance using the drone's new position
        """
        dy = update_data.get_haversine_distance() * sin(update_data.get_heading())
        dx = update_data.get_haversine_distance() * cos(update_data.get_heading())
        new_drone_location = np.array([dx, dy])#, update_data.get_altitude()])
        self.obstacle_map.set_drone_position(new_drone_location)

        obstacle_in_path_boolean, avoid_coords = self.obstacle_map.is_obstacle_in_path()
        if obstacle_in_path_boolean:
            min_tangent_point = self.obstacle_map.get_min_tangent_point(avoid_coords)

            if VectorMath.get_magnitude(self.previous_min_tangent_point, min_tangent_point) > self.minimum_change_in_guided_point:
                bearing = atan2(min_tangent_point[0], min_tangent_point[1])
                self.previous_min_tangent_point = min_tangent_point

                return inverse_haversine(self.get_initial_coordinates(), [min_tangent_point[0], min_tangent_point[1], update_data.get_altitude()], bearing)

        return None

    def get_obstacle_map(self):
        return self.obstacle_map
