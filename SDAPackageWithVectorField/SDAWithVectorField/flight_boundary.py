from matplotlib.path import Path

class FlightBoundary(object):
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
        :type boundary_waypoints: Numpy Array
        """
        self.min_altitude = min_altitude
        self.max_altitude = max_altitude
        self.bound_path = Path(boundary_waypoints)

    def is_point_in_bounds(self, point):
        """
        Returns True if the passed point is in the boundaries, False if not

        :param point: The point to test
        :type point: Numpy Array
        """
        dim_reduced_point = point[:2]
        is_point_in_polygon = self.path_method(dim_reduced_point)
        is_point_in_alts = (point[2] > self.min_altitude and point[2] < self.max_altitude)

        if is_point_in_polygon and is_point_in_alts:
            return True

        return False

    def path_method(self, point):
        """
        Returns True if the point is within the flight boundary, False if
        not

        :param point: The point to test
        :type point: Numpy Array
        """
        return self.bound_path.contains_points([point])