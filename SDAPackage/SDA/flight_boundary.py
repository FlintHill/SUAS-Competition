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
        self.boundary_path = boundary_waypoints

    def is_point_in_bounds(self, point):
        """
        Returns True if the passed point is in the boundaries, False if not

        :param point: The point to test
        :type point: Numpy Array
        """
        dim_reduced_point = point[:2]
        is_point_in_polygon = self.ray_tracing_method(dim_reduced_point[0], dim_reduced_point[1])
        is_point_in_alts = (point[2] > self.min_altitude and point[2] < self.max_altitude)

        if is_point_in_polygon and is_point_in_alts:
            return True

        return False

    def ray_tracing_method(self, x,y):
        """
        Returns True if the point is in the bounding polygon, false if it is
        outside of it.

        :param x: The X-coordinate of the point
        :type x: int
        :param y: They Y-coordinate of the point
        :type y: int
        """
        poly = self.boundary_path
        n = len(poly)
        inside = False

        p1x,p1y = poly[0]
        for i in range(n+1):
            p2x,p2y = poly[i % n]
            if y > min(p1y,p2y):
                if y <= max(p1y,p2y):
                    if x <= max(p1x,p2x):
                        if p1y != p2y:
                            xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                            if p1x == p2x or x <= xints:
                                inside = not inside
            p1x,p1y = p2x,p2y

        return inside
