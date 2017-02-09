from ObjAvoid import MultiDimPoint
import static_math
from math import sin, cos

class Waypoint(gps_coordinates):
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
        gps_coordinates.__init__(lat, lng, alt)
        
        
    
    
    
    '''
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
    '''
        
    '''not sure if origin GPS is in lon, lat, or lat, lon'''
    def convert_to_point(self, originGPS):
        haversineDistance = static_math.haversine(originGPS, self)
        bearing = static_math.bearing(originGPS, self)
        dx = haversineDistance * cos(bearing)
        dy = haversineDistance * sin(bearing)
        return MultiDimPoint([dx,dy,self.get_altitude())
