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
        self.drone = Drone(np.array([0,0]), np.array([]))

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
        self.drone.reset_waypoint_holder()

    def is_obstacle_in_path(self):
        """
        Return True if drone should avoid obstacle and False if not
        """
        current_waypoint = self.drone.get_waypoint_holder().get_current_waypoint()
        drone_point = self.drone.get_point()

        waypoint_vector = np.subtract(current_waypoint, drone_point)
        for obstacle in self.obstacles.tolist():
            obstacle_vector = np.subtract(obstacle.get_point(), drone_point)
            obstacle_vector_magnitude = VectorMath.get_vector_magnitude(obstacle_vector)
            projection_vector = VectorMath.get_vector_projection(obstacle_vector, waypoint_vector)
            projection_vector_from_obstacle = np.subtract(obstacle_vector, projection_vector)
            projection_vector_from_obstacle_magnitude = VectorMath.get_vector_magnitude(projection_vector_from_obstacle)

            if projection_vector_from_obstacle_magnitude < obstacle.get_radius():
                if self.is_obstacle_in_path_of_drone(obstacle_vector, waypoint_vector):
                    # Uncomment for DEBUGGING ONLY
                    #print("Waypoint Vector: " + str(waypoint_vector))
                    #print("Obstacle Vector: " + str(obstacle_vector))
                    #print("Projection Vector: " + str(projection_vector))
                    #print("Projection Vector From Obstacle: " + str(projection_vector_from_obstacle))
                    #print("Projection Vector From Obstacle Magnitude: " + str(projection_vector_from_obstacle_magnitude))
                    #print("Obstacle Safety Radius: " + str(obstacle.get_safety_radius()))

                    angle = atan2(-1.0 * waypoint_vector[0], waypoint_vector[1])

                    perp_point_x = obstacle.get_radius() * cos(angle)
                    perp_point_y = obstacle.get_radius() * sin(angle)
                    tangent_point_one = np.array([obstacle.get_point()[0] + perp_point_x, obstacle.get_point()[1] + perp_point_y])

                    angle += pi % (2 * pi)
                    perp_point_x = obstacle.get_radius() * cos(angle)
                    perp_point_y = obstacle.get_radius() * sin(angle)
                    tangent_point_two = np.array([obstacle.get_point()[0] + perp_point_x, obstacle.get_point()[1] + perp_point_y])

                    # Uncomment for DEBUGGING ONLY
                    #print("Tangent Point One: " + str(tangent_point_one))
                    #print("Tangent Point Two: " + str(tangent_point_two))

                    return True, np.array([tangent_point_one, tangent_point_two])

        return False, None

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

    def get_min_tangent_point(self, points):
        """
        Return the shortest tangent point from the points provided. This function assumes
        that the paths are possible waypoints calculated from the is_obstacle_in_path()
        function

        :param points: The points to determine the minimum distance of
        :type points: Numpy Array
        """
        shortest_tangent_point = points[0]
        shortest_distance = self.get_path_distance(points[0])

        for tangent_point in points.tolist()[1:]:
            distance = self.get_path_distance(tangent_point)

            if distance < shortest_distance:
                shortest_tangent_point = np.array(tangent_point)
                shortest_distance = distance

        return shortest_tangent_point

    def get_path_distance(self, tangent_point):
        """
        Get the path distance from drone point to path point to current waypoint

        :param tangent_point: The tangent point to calculate distance from
        :type tangent_point: Numpy Array
        """
        first_leg_distance = VectorMath.get_magnitude(self.drone.get_point(), tangent_point)
        second_leg_distance = VectorMath.get_magnitude(tangent_point, self.drone.get_waypoint_holder().get_current_waypoint())

        return first_leg_distance + second_leg_distance

    def get_obstacles(self):
        """
        Return the obstacles in the map
        """
        return self.obstacles

    def get_drone(self):
        """
        Return the drone
        """
        return self.drone
