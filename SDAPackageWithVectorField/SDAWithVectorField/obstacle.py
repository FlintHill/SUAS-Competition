from abc import abstractmethod
from abc import ABCMeta

class Obstacle(object):
    """
    Abstract class for obstacles
    """

    __metaclass__ = ABCMeta

    def __init__(self, point):
        """
        :param point: The location of the Obstacle
        :type point: Numpy Array
        """
        self.point = point

    def get_point(self):
        """
        Return the point
        """
        return self.point
