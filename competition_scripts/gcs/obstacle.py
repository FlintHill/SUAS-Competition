class Obstacle:
    """
    Wrapper class for obstacles
    """

    def __init__(self, dist, heading, alt, radius, obstacle_type):
        """
        Initialize

        :param dist: The haversine distance from the origin to the obstacle
        :param heading: The heading calculated from the origin to the obstacle
        :param alt: The altitude of the obstacle
        :param radius: The radius of the obstacle
        :param obstacle_type: The type of the obstacle (either stationary or
            moving)
        """
        self.dist = dist
        self.heading = heading
        self.alt = alt
        self.radius = radius
        self.type = obstacle_type

    def get_distance(self):
        """
        Return the distance
        """
        return self.dist

    def get_heading(self):
        """
        Return the heading
        """
        return self.heading

    def get_altitude(self):
        """
        Return the altitude
        """
        return self.alt

    def get_radius(self):
        """
        Return the radius
        """
        return self.radius

    def get_obstacle_type(self):
        """
        Return the obstacle's type
        """
        return self.type
