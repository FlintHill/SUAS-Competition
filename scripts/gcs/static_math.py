from math import radians, cos, sin, asin, sqrt, acos, atan2, degrees, pi
import math
from gps_coordinates import GPSCoordinates

def haversine(gps1, gps2):
    """
    Calculates the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    dy = (gps2.get_latitude() - gps1.get_latitude()) * 69.172 * 1609.34
    dx = (gps2.get_longitude() - gps1.get_longitude()) * 69.172 * cos((gps1.get_latitude() + gps2.get_latitude()) * pi / 360.0) * 1609.34

    dist = (dy**2 + dx**2)**0.5 * 0.999

    return dist

def point_in_polygon(polygon, point):
    """
    Returns True if the point is in the polygon, and false if it is
    outside of it.

    :param polygon: A list of points that are the polygon corners
    :param point: The point to determine its location
    """
    for corner in polygon:
        pass

def inverse_haversine(gps1, dist, alt_diff, bearing):
    """
    Calculate a second GPS point through using a single GPS point and a
    different in XY units

    :param gps1: The first GPS coordinate
    :type gps1: GPSCoordinates
    :param diff: The difference in the [dX, dY, alt]
    :param bearing: The bearing between the two points
    """
    alt = gps1.get_altitude() + alt_diff

    diff_magnitude = dist / 1000.1
    lat = gps1.get_latitude() + (diff_magnitude * cos(bearing) / 111.195)
    lon = gps1.get_longitude() + ((diff_magnitude * sin(bearing)) / (cos(math.radians((lat + gps1.get_latitude()) / 2.0)) * 111.191))

    return GPSCoordinates(lat, lon, alt)

def bearing(gps1, gps2):
    """
    Calculates the bearing between two points
    """
    lat1 = gps1.get_latitude_radians()
    lat2 = gps2.get_latitude_radians()

    diffLong = math.radians(gps2.get_longitude() - gps1.get_longitude())

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    return initial_bearing
