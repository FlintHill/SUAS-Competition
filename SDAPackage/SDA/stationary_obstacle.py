from SDA import Obstacle
from SDA import Constants

class StationaryObstacle(Obstacle):
    """
    Wrapper class for Stationary obstacles
    """

    def __init__(self, point, radius):
        """
        :param point: The point for the stationary obstacle
        :type point: Numpy Array
        """
        super(StationaryObstacle, self).__init__(point, Constants.STATIONARY_OBSTACLE_SAFETY_RADIUS)

        self.radius = radius

    def get_radius(self):
        """
        Return the radius of the obstacle plus that of the safety radius
        """
        return self.radius + self.get_safety_radius()
