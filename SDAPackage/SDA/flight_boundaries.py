class FlightBoundaries(object):
    """
    Provides an interface for flight zone boundaries
    """

    def __init__(self, min_altitude, max_altitude, boundary_waypoints):
        """
        Initialize the flight boundaries object with the different requirements

        :param min_altitude: The minimum flying altitude
        :type min_altitude: Float
        :param max_altitude: The maximum flying altitude
        :type max_altitude: Float
        :param boundary_waypoints: The boundary waypoints. Outside of this polygon
            of waypoints exists the no flight zone
        """
        self.min_altitude = min_altitude
        self.max_altitude = max_altitude
        self.boundary_waypoints = boundary_waypoints

    def is_point_in_bounds(self, point):
        """
        Returns True if the passed point is in the boundaries, False if not

        :param point: The point to test
        :type point: Numpy Array
        """
        is_point_in_polygon = self.point_in_polygon(point)
        is_point_in_alts = (point[2] > self.min_altitude and point[2] < self.max_altitude)

        if is_point_in_polygon and is_point_in_alts:
            return True

        return False

    def point_in_polygon(self, point):
        """
        Returns True if the point is in the polygon, and false if it is
        outside of it.

        :param point: The point to determine its location
        :type point: Numpy Array
        """
        for corner in polygon:
            pass
