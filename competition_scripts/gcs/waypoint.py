class Waypoint:
    """
    Wrapper class for transporting waypoints between the main client
    script and the converter class
    """

    def __init__(self, lat, lng, alt):
        """
        Initialize

        :param lat: The latitude of the waypoint
        :param lng: The longtitude of the waypoint
        :param alt: The altitude of the waypoint
        """
        self.lat = lat
        self.lng = lng
        self.alt = alt

    def get_latitude(self):
        """
        Returns the latitude of the waypoint
        """
        return self.lat

    def get_longitude(self):
        """
        Returns the longitude of the waypoint
        """
        return self.lng

    def get_alt(self):
        """
        Returns the altitude of the waypoint
        """
        return self.alt
