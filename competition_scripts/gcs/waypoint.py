from ObjAvoid import MultiDimPoint
from gps_coordinates import GPSCoordinates
import static_math
from math import sin, cos

class Waypoint(GPSCoordinates):
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
        super(Waypoint, self).__init__(lat, lng, alt)

    def convert_to_point(self, originGPS):
        haversineDistance = static_math.haversine(originGPS, self)
        bearing = static_math.bearing(originGPS, self)
        dx = haversineDistance * cos(bearing)
        dy = haversineDistance * sin(bearing)
        return MultiDimPoint([dx,dy,self.get_altitude()])
