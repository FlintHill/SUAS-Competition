class ConverterDataUpdate:
    """
    Wrapper for data sent between the client code and the VectorNavAvoidance
    converter
    """

    def __init__(self, haversine_distance, heading, altitude):
        """
        Initialize

        :param haversine_distance: The haversine distance from the initial
            drone location to its current location
        :param heading: The UAV's current heading
        :param altitude: The UAV's current altitude
        """
        self.haversine_distance = haversine_distance
        self.heading = heading
        self.altitude = altitude

    def get_haversine_distance(self):
        """
        Return the haversine distance
        """
        return self.haversine_distance

    def get_heading(self):
        """
        Return the heading
        """
        return self.heading

    def get_altitude(self):
        """
        Return altitude
        """
        return self.altitude
