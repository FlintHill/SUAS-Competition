class Drone(object):
    """
    Wrapper for drone
    """

    def __init__(self, point):
        """
        :param point: The starting point of the drone
        :param type: Numpy Array
        """
        self.point = point

    def get_point(self):
        """
        Return point
        """
        return self.point
