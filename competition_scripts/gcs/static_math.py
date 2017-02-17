from math import radians, cos, sin, asin, sqrt, acos, atan2
from gps_coordinates import GPSCoordinates

def haversine(gps1, gps2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [gps1.get_longitude(), gps1.get_latitude(), gps2.get_longitude(), gps2.get_latitude()])

    # haversine formula
    dlon = gps2.get_longitude() - gps1.get_longitude()
    dlat = gps2.get_latitude() - gps1.get_latitude()
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def inverse_haversine(gps1, diff, bearing):
    """
    Calculate a second GPS point through using a single GPS point and a
    different in XY units

    :param gps1: The first GPS coordinate
    :type gps1: GPSCoordinates
    :param diff: The difference in the [dX, dY, alt]
    :param bearing: The bearing between the two points
    """
    alt = gps1.get_altitude() + diff[2]

    diff_magnitude = float((diff[1]**2 + diff[0]**2)**0.5)
    lat = gps1.get_latitude() + (diff_magnitude * cos(bearing) / 111.2)
    lon = gps1.get_longitude()
    lon += ((diff_magnitude * sin(bearing) / (cos(lat) * 111.321)) + (diff_magnitude * sin(bearing)  (cos(gps1.get_latitude()) * 111.321))) / 2.0

    return GPSCoordinates(lat, lon, alt)

def bearing(gps1, gps2):
    bearing = atan2(sin(gps2.get_longitude()-gps1.get_longitude())*cos(gps2.get_longitude()), cos(gps1.get_latitude())*sin(gps2.get_longitude())-sin(gps1.get_latitude())*cos(gps2.get_latitude())*cos(gps2.get_longitude()-gps1.get_longitude()))
    return bearing
