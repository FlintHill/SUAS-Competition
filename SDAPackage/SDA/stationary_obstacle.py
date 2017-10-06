from SDA import Obstacle
from SDA import Constants

class StationaryObstacle(Obstacle):
    """
    Wrapper class for Stationary obstacles
    """

    def __init__(self, point, radius, height):
        """
        :param point: The point for the stationary obstacle
        :type point: Numpy Array
        :param radius: The radius of the obstacle
        :type radius: Float
        :param height: The height of the obstacle
        :type height: Float
        """
        super(StationaryObstacle, self).__init__(point, Constants.STATIONARY_OBSTACLE_SAFETY_RADIUS)

        self.radius = radius
        self.height = height

    def get_radius(self):
        """
        Return the radius of the obstacle plus that of the safety radius
        """
        return self.radius + self.get_safety_radius()

    def get_height(self):
        """
        The height of the obstacle
        """
        return self.height

    def make_avoidance_points(self, drone_altitude):
        """

        :param drone_altitude: The altitude of the drone
        :type drone_altitude: Float
        """
        new_avoidance_pos_points = [
            [self.get_point()[0] + self.get_radius(), self.get_point()[1] + self.get_radius(), drone_altitude],
            [self.get_point()[0] - self.get_radius(), self.get_point()[1] - self.get_radius(), drone_altitude],
            [self.get_point()[0] + self.get_radius(), self.get_point()[1] - self.get_radius(), drone_altitude],
            [self.get_point()[0] - self.get_radius(), self.get_point()[1] + self.get_radius(), drone_altitude],
            [self.get_point()[0], self.get_point()[1] + self.get_radius(), self.get_height() + (Constants.STATIONARY_OBSTACLE_SAFETY_RADIUS * 2)],
            [self.get_point()[0], self.get_point()[1] - self.get_radius(), self.get_height() + (Constants.STATIONARY_OBSTACLE_SAFETY_RADIUS * 2)],
            [self.get_point()[0] + self.get_radius(), self.get_point()[1], self.get_height() + (Constants.STATIONARY_OBSTACLE_SAFETY_RADIUS * 2)],
            [self.get_point()[0] - self.get_radius(), self.get_point()[1], self.get_height() + (Constants.STATIONARY_OBSTACLE_SAFETY_RADIUS * 2)]
        ]

        return new_avoidance_pos_points
