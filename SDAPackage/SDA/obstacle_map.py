import numpy as np
from math import atan2, cos, sin, pi
from SDA import Drone
from SDA import StationaryObstacle
from SDA import VectorMath

class ObstacleMap(object):
    """
    Wrapper class for an obstacle map
    """

    def __init__(self):
        self.obstacles = np.array([])
        self.drone = Drone(np.array([0,0,0]), np.array([]))

    def add_obstacle(self, obstacle_to_add):
        """
        Add an obstacle to the map

        :param obstacle_to_add: The obstacle to add to the map
        :type obstacle_to_add: StationaryObstacle
        """
        if self.obstacles.size != 0:
            self.obstacles = np.vstack([self.obstacles, obstacle_to_add])
        else:
            self.obstacles = np.array([obstacle_to_add])

    def add_waypoint(self, waypoint):
        """
        Add a waypoint to the drone

        :param waypoint: The waypoint to add
        :type waypoint: Numpy Array
        """
        self.drone.add_waypoint(waypoint)

    def set_drone_position(self, new_point):
        """
        Set the drone's location in the map

        :param new_point: The new point for the drone
        :type new_point: Numpy Array
        """
        self.drone.set_drone_position(new_point)

    def reset_obstacles(self):
        """
        Reset the obstacles' positions within the map (should be called
        when map is refreshed to clean the array)
        """
        self.obstacles = np.array([])

    def reset_waypoints(self):
        """
        Reset the waypoints
        """
        self.drone.reset_waypoints()

    def is_obstacle_in_path(self):
        """
        Return True if drone should avoid obstacle and False if not
        """
        drone_point = self.drone.get_point()

        for obstacle in self.obstacles.tolist():
            if self.does_point_intersect_obstacle(obstacle, drone_point, self.drone.get_waypoint_holder().get_current_waypoint()):
                new_attempt_pos_points = [
                    [obstacle.get_point()[0] + obstacle.get_radius(), obstacle.get_point()[1] + obstacle.get_radius(), 0],
                    [obstacle.get_point()[0] - obstacle.get_radius(), obstacle.get_point()[1] - obstacle.get_radius(), 0],
                    [obstacle.get_point()[0] + obstacle.get_radius(), obstacle.get_point()[1] - obstacle.get_radius(), 0],
                    [obstacle.get_point()[0] - obstacle.get_radius(), obstacle.get_point()[1] + obstacle.get_radius(), 0]
                ]

                new_paths = []
                for new_pos_point in new_attempt_pos_points:
                    if not self.does_point_intersect_obstacle(obstacle, drone_point, new_pos_point):
                        for recursive_new_pos_point in new_attempt_pos_points:
                            if not self.does_point_intersect_obstacle(obstacle, new_pos_point, recursive_new_pos_point) and not self.does_point_intersect_obstacle(obstacle, recursive_new_pos_point, self.drone.get_waypoint_holder().get_current_waypoint()):
                                new_paths.append([new_pos_point, recursive_new_pos_point])

                # Uncomment for DEBUGGING ONLY
                #for path in new_paths:
                #    print("Point:", str(path))

                return True, np.array(new_paths)

        return False, None

    def does_point_intersect_obstacle(self, obstacle, drone_point, waypoint):
        """
        Determine if the vector between a UAV's position and the current waypoint intersect
        an obstacle.

        :param obstacle: The obstacle to determine if the UAV intersects with
        :type obstacle: StationaryObstacle or MovingObstacle
        :param drone_point: The UAV's position
        :type drone_point: Numpy Array
        :param waypoint: The waypoint that the UAV is headed to
        :type waypoint: Numpy Array
        """
        waypoint_vector = np.subtract(waypoint, drone_point)
        obstacle_vector = np.subtract(obstacle.get_point(), drone_point)
        obstacle_vector_magnitude = VectorMath.get_vector_magnitude(obstacle_vector)
        rejection_vector = VectorMath.get_vector_rejection(obstacle_vector, waypoint_vector)
        rejection_vector_magnitude = VectorMath.get_vector_magnitude(rejection_vector)

        # Uncomment for DEBUGGING ONLY
        #print("Waypoint Vector: " + str(waypoint_vector))
        #print("Obstacle Vector: " + str(obstacle_vector))
        #print("Rejection Vector: " + str(rejection_vector))
        #print("Rejection Vector Magnitude: " + str(rejection_vector_magnitude))
        #print("Obstacle Safety Radius: " + str(obstacle.get_safety_radius()))

        if self.is_obstacle_in_path_of_drone(obstacle_vector, waypoint_vector):
            return rejection_vector_magnitude < obstacle.get_radius()

        return False

    def is_obstacle_in_path_of_drone(self, obstacle_vector, waypoint_vector):
        """
        Looks at the signs of the components of the vectors to determine if the
        direction of the obstacle is in the same direction as the waypoint
        (quadrants)
        """
        obstacle_list = obstacle_vector.tolist()
        waypoint_list = waypoint_vector.tolist()

        for index in range(len(obstacle_list)):
            if all(item > 0 for item in [-1.0 * obstacle_list[index], waypoint_vector[index]]) or all(item < 0 for item in [-1.0 * obstacle_list[index], waypoint_vector[index]]):
                return False

        return True

    def get_min_path(self, paths):
        """
        Return the shortest path from the paths provided. This function assumes
        that the paths are possible waypoints calculated from the is_obstacle_in_path()
        function

        :param paths: The paths to determine the minimum distance of
        :type paths: Numpy Array
        """
        shortest_path = paths[0]
        shortest_distance = self.get_path_distance(paths[0])

        for path in paths[1:]:
            distance = self.get_path_distance(path)

            if distance < shortest_distance:
                shortest_path = path
                shortest_distance = distance

        return shortest_path

    def get_path_distance(self, path):
        """
        Get the path distance from drone point to path points to current
        waypoint. It will find the distance of a n-length path

        :param path: The path to calculate distance of
        :type path: Numpy Array
        """
        distance = VectorMath.get_magnitude(self.drone.get_point(), path[0])
        for index in range(len(path[:-1])):
            distance += VectorMath.get_magnitude(path[index], path[index + 1])
        distance += VectorMath.get_magnitude(path[-1], self.drone.get_waypoint_holder().get_current_waypoint())

        return distance

    def get_obstacles(self):
        """
        Return the obstacles in the map
        """
        return self.obstacles

    def has_uav_reached_current_waypoint(self):
        """
        Return True if the UAV has reached the current waypoint and false if not
        """
        return self.drone.has_reached_waypoint()

    def get_drone(self):
        """
        Return the drone
        """
        return self.drone
