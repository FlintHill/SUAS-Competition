class CurrentCoordinates:
    """
    Wrapper class for the drone's current coordinates
    """

    def __init__(self, latitude, longitude, altitude, heading):
        """
        Initialize

        :param latitude: The current latitude of the UAV
        :param longitude: The current longitude of the UAV
        :param altitude: The current altitude of the UAV
        :param heading: The current heading of the UAV
        """
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.heading = heading

    def get_latitude(self):
        """
        Return the latitude
        """
        return self.latitude

    def get_longitude(self):
        """
        Return longitude
        """
        return self.longitude

    def get_altitude(self):
        """
        Return altitude
        """
        return self.altitude

    def get_heading(self):
        """
        Return heading
        """
        return self.heading
