from abc import abstractmethod
from abc import ABCMeta

class Obstacle(object):
    """
    Abstract class for obstacles
    """

    __metaclass__ = ABCMeta

    def __init__(self, point, safety_radius):
        """
        :param point: The location of the Obstacle
        :type point: Numpy Array
        """
        self.point = point
        self.safety_radius = safety_radius


    def get_safety_radius(self):
        """
        Return the safety radius
        """
        return self.safety_radius

    def get_point(self):
        """
        Return the point
        """
        return self.point
