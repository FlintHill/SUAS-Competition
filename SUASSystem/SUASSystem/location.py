from dronekit import LocationGlobalRelative

class Location(object):
    """
    Wrapper class for DroneKit's LocationGlobalRelative class
    """

    def __init__(self, lat, lon, alt):
        """
        Initialize the Location instance

        :param lat: The latitude of the location in degrees
        :type lat: Float
        :param lon: The longitude of the location in degrees
        :type lon: Float
        :param alt: The altitude of the location in meters
        :type alt: Float
        """
        self.lat = lat
        self.lon = lon
        self.alt = alt

        self.location = LocationGlobalRelative(self.lat, self.lon, self.alt)

    def get_lat(self):
        """
        Get the latitude of the location
        """
        return self.lat

    def get_lon(self):
        """
        Get the longitude of the location
        """
        return self.lon

    def get_alt(self):
        """
        Get the altitude of the location
        """
        return self.alt

    def as_global_relative_frame(self):
        """
        Get the LocationGlobalRelative form of this location
        """
        return self.location

    def __repr__(self):
        return "Lat: " + str(self.get_lat()) + " Lon: " + str(self.get_lon()) + " Alt: " + str(self.get_alt())
