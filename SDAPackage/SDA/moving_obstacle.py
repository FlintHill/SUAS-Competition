from SDA import Obstacle
from SDA import Constants

class MovingObstacle(Obstacle):
    """
    Wrapper class for Moving obstacles
    """

    def __init__(self, point, radius, speed):
        """
        :param point: The point for the moving obstacle
        :type point: Numpy Array
        """
        super(MovingObstacle, self).__init__(point, Constants.STATIONARY_OBSTACLE_SAFETY_RADIUS)

        self.radius = radius
        self.speed = speed

    def get_radius(self):
        """
        Return the radius of the obstacle plus that of the safety radius
        """
        return (self.radius + self.get_safety_radius()) * self.speed / 10.0

    def get_speed(self):
        """
        Returns the speed of the obstacle
        """
        return self.speed
