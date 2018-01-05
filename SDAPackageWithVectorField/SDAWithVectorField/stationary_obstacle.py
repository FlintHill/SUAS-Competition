from SDAWithVectorField import Obstacle
from SDAWithVectorField import Constants

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
        super(StationaryObstacle, self).__init__(point)

        self.radius = radius
        self.height = height
        self.type = "stationary"

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

    def get_type(self):
        return self.type
