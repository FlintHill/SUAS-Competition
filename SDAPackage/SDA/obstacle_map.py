import numpy as np
from math import atan2, cos, sin, pi
from SDA import *

class ObstacleMap(object):
    """
    Wrapper class for an obstacle map
    """

    def __init__(self, drone_point, fly_zones):
        """
        Initialize

        :param drone_point: The UAV's starting location
        :type drone_point: Numpy Array
        :param fly_zones: The fly zones for the UAV
        :type fly_zones: Numpy Array
        """
        self.obstacles = np.array([])
        self.drone = Drone(drone_point, np.array([]))
        self.flight_boundary = FlightBoundariesContainer(fly_zones)

    def add_obstacle(self, obstacle_to_add):
        """
        Add an obstacle to the map

        :param obstacle_to_add: The obstacle to add to the map
        :type obstacle_to_add: StationaryObstacle
        """
        if self.obstacles.size != 0:
            self.obstacles = np.hstack((self.obstacles, obstacle_to_add))
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
        for obstacle in self.obstacles.tolist():
            print("obstacle.get_point():", obstacle.get_point())
            dist_to_obstacle = VectorMath.get_vector_magnitude(np.subtract(obstacle.get_point(), self.drone.get_point()))
            if dist_to_obstacle < obstacle.get_radius() + Constants.DETECTION_THRESHOLD:
                if isinstance(obstacle, StationaryObstacle):
                    paths = self.generate_possible_paths(obstacle)

                    if len(paths) != 0:
                        return True, np.array(paths)
                elif isinstance(obstacle, MovingObstacle):
                    pass

        return False, None

    def generate_possible_paths(self, obstacle):
        """
        Generate possible paths around the passed obstacle

        :param obstacle: The obstacle to generate paths around
        :type obstacle: StationaryObstacle or MovingObstacle
        """
        if self.does_uav_intersect_obstacle_vertically(obstacle, self.drone.get_point(), self.drone.get_waypoint_holder().get_current_waypoint()):
            if self.does_path_intersect_obstacle_2d(obstacle, self.drone.get_point(), self.drone.get_waypoint_holder().get_current_waypoint()):
                new_attempt_pos_points = [
                    [obstacle.get_point()[0] + obstacle.get_radius(), obstacle.get_point()[1] + obstacle.get_radius(), self.drone.get_point()[2]],
                    [obstacle.get_point()[0] - obstacle.get_radius(), obstacle.get_point()[1] - obstacle.get_radius(), self.drone.get_point()[2]],
                    [obstacle.get_point()[0] + obstacle.get_radius(), obstacle.get_point()[1] - obstacle.get_radius(), self.drone.get_point()[2]],
                    [obstacle.get_point()[0] - obstacle.get_radius(), obstacle.get_point()[1] + obstacle.get_radius(), self.drone.get_point()[2]],
                    [obstacle.get_point()[0], obstacle.get_point()[1] + obstacle.get_radius(), obstacle.get_height() + (Constants.STATIONARY_OBSTACLE_SAFETY_RADIUS * 2)],
                    [obstacle.get_point()[0], obstacle.get_point()[1] - obstacle.get_radius(), obstacle.get_height() + (Constants.STATIONARY_OBSTACLE_SAFETY_RADIUS * 2)],
                    [obstacle.get_point()[0] + obstacle.get_radius(), obstacle.get_point()[1], obstacle.get_height() + (Constants.STATIONARY_OBSTACLE_SAFETY_RADIUS * 2)],
                    [obstacle.get_point()[0] - obstacle.get_radius(), obstacle.get_point()[1], obstacle.get_height() + (Constants.STATIONARY_OBSTACLE_SAFETY_RADIUS * 2)]
                ]

                new_paths = []
                print("before new_pos_point")
                for new_pos_point in new_attempt_pos_points:
                    print("IN new_pos_point")
                    if not self.does_path_intersect_obstacle_3d(obstacle, self.drone.get_point(), new_pos_point) and self.flight_boundary.is_point_in_bounds(new_pos_point):
                        print("does_path_intersect_obstacle_3d")
                        for recursive_new_pos_point in new_attempt_pos_points:
                            print("recursive_new_pos_point")
                            if self.flight_boundary.is_point_in_bounds(recursive_new_pos_point) and abs(recursive_new_pos_point[2] - new_pos_point[2]) < 5:
                                if recursive_new_pos_point[0] != new_pos_point[0] or recursive_new_pos_point[1] != new_pos_point[1]:
                                    if not self.does_path_intersect_obstacle_3d(obstacle, new_pos_point, recursive_new_pos_point) and not self.does_path_intersect_obstacle_3d(obstacle, recursive_new_pos_point, self.drone.get_waypoint_holder().get_current_waypoint()):
                                        new_paths.append([new_pos_point, recursive_new_pos_point])

                # Uncomment for DEBUGGING ONLY
                for path in new_paths:
                    print("Point:", str(path))

                print("RETURNING NEW PATHS")
                return new_paths

        print("RETURNING NOTHING")
        return []

    def does_uav_intersect_obstacle_vertically(self, obstacle, drone_point, waypoint):
        """
        Determine if the UAV intersects an obstacle on the verticle axis

        :param obstacle: The obstacle that the UAV could intersect
        :type obstacle: StationaryObstacle or MovingObstacle
        :param drone_point: The UAV's current position
        :type drone_point: Numpy Array
        :param waypoint: The waypoint for the UAV
        :type waypoint: Numpy Array
        """
        if isinstance(obstacle, StationaryObstacle):
            if drone_point[2] < obstacle.height + Constants.STATIONARY_OBSTACLE_SAFETY_RADIUS:
                return True

        return False

    def does_path_intersect_obstacle_2d(self, obstacle, uav_point, waypoint):
        """
        Determine if the vector between a UAV's position and the current waypoint intersect
        an obstacle.

        :param obstacle: The obstacle to determine if the UAV intersects with
        :type obstacle: StationaryObstacle or MovingObstacle
        :param uav_point: The UAV's position
        :type uav_point: Numpy Array
        :param waypoint: The waypoint that the UAV is headed to
        :type waypoint: Numpy Array
        """
        drone_point = uav_point[:-1]
        waypoint = waypoint[:-1]
        obstacle_point = obstacle.get_point()[:-1]

        waypoint_vector = np.subtract(waypoint, drone_point)
        obstacle_vector = np.subtract(obstacle_point, drone_point)
        obstacle_vector_magnitude = VectorMath.get_vector_magnitude(obstacle_vector)
        rejection_vector = VectorMath.get_vector_rejection(obstacle_vector, waypoint_vector)
        rejection_vector_magnitude = VectorMath.get_vector_magnitude(rejection_vector)

        # Uncomment for DEBUGGING ONLY
        print("Waypoint Vector: " + str(waypoint_vector))
        print("Obstacle Vector: " + str(obstacle_vector))
        print("Rejection Vector: " + str(rejection_vector))
        print("Rejection Vector Magnitude: " + str(rejection_vector_magnitude))
        print("Obstacle Radius: " + str(obstacle.get_radius()))
        print("Distance From Obstacle: " + str(VectorMath.get_vector_magnitude(np.subtract(uav_point, obstacle.get_point()))))

        if self.is_obstacle_in_path_of_drone(obstacle_vector, waypoint_vector):
            return rejection_vector_magnitude < obstacle.get_radius()

        return False

    def does_path_intersect_obstacle_3d(self, obstacle, drone_point, waypoint):
        """
        Determine if the vector between a UAV's position and the current waypoint intersect
        an obstacle.

        :param obstacle: The obstacle to determine if the UAV intersects with
        :type obstacle: StationaryObstacle or MovingObstacle
        :param uav_point: The UAV's position
        :type uav_point: Numpy Array
        :param waypoint: The waypoint that the UAV is headed to
        :type waypoint: Numpy Array
        """
        waypoint_vector = np.subtract(waypoint, drone_point)
        obstacle_vector = np.subtract(obstacle.get_point(), drone_point)
        obstacle_vector_magnitude = VectorMath.get_vector_magnitude(obstacle_vector)
        rejection_vector = VectorMath.get_vector_rejection(obstacle_vector, waypoint_vector)
        rejection_vector_magnitude = VectorMath.get_vector_magnitude(rejection_vector)

        # Uncomment for DEBUGGING ONLY
        print("Waypoint Vector: " + str(waypoint_vector))
        print("Obstacle Vector: " + str(obstacle_vector))
        print("Rejection Vector: " + str(rejection_vector))
        print("Rejection Vector Magnitude: " + str(rejection_vector_magnitude))
        print("Obstacle Radius: " + str(obstacle.get_radius()))
        print("Distance From Obstacle: " + str(VectorMath.get_vector_magnitude(np.subtract(drone_point, obstacle.get_point()))))

        if self.is_obstacle_in_path_of_drone(obstacle_vector, waypoint_vector):
            return rejection_vector_magnitude < Constants.STATIONARY_OBSTACLE_SAFETY_RADIUS

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

        if abs(self.drone.get_point()[2] - path[0][2]) > 1:
            distance *= Constants.VERTICAL_PATH_WEIGHTING_MULTIPLE

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
