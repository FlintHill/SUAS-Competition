from SDA import Obstacle
from SDA import Constants

class StationaryObstacle(Obstacle):
    """
    Wrapper class for Stationary obstacles
    """

    def __init__(self, point):
        """
        :param point: The point for the stationary obstacle
        :type point: Numpy Array
        """
        super(StationaryObstacle, self).__init__(point, Constants.STATIONARY_OBSTACLE_SAFETY_RADIUS)
