from SDAWithVectorField import *
import numpy

class FlightBoundariesContainer(object):

    def __init__(self, fly_zones):
        """
        Initialize a set of fly zones

        :param fly_zones: The fly zones for the UAV
        :type fly_zones: Numpy Array
        """
        self.fly_zones = numpy.array([FlightBoundary(Constants.MIN_ALT, Constants.MAX_ALT, boundary_points) for boundary_points in fly_zones])

    def is_point_in_bounds(self, point):
        """
        Determine whether the point is located within one of the fly zones

        :param point: The point to test
        :type point: Numpy Array
        """
        for index in range(self.fly_zones.shape[0]):
            if self.fly_zones[index].is_point_in_bounds(point):
                return True

        return False
