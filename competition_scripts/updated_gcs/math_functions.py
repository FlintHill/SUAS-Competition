from location_data import Location
import math

def haversine(location1, location2, units="METRIC"):
    """
    Calculates the great circle distance between two points
    on the earth (specified in decimal degrees)

    :param location1: The first GPS location
    :type location1: Location
    :param location2: The second GPS location
    :type location2: Location
    """
    dz = location2.get_alt() - location1.get_alt()
    dy = (location2.get_lat() - location1.get_lat()) * 69.172
    dx = (location2.get_lon() - location1.get_lon()) * 69.172 * math.cos(math.radians(location1.get_lat() + location2.get_lat()) / 2)

    if "metric" in units.lower():
        dy *= 1609.34
        dx *= 1609.34
    elif "us" in units.lower():
        dy *= 1609.34 * 3.28084
        dx *= 1609.34 * 3.28084

    dist = (dy**2 + dx**2 + dz**2)**0.5 * 0.999
    return dist

def point_in_polygon(polygon, point):
    """
    Returns True if the point is in the polygon, and false if it is
    outside of it.

    :param polygon: A list of points that are the polygon corners
    :param point: The point to determine its location
    """
    # TODO Fill in this method
    for corner in polygon:
        pass

def inverse_haversine(location1, point, uav_bearing):
    """
    Calculate a second GPS point through using a single GPS point and a
    different in XY units

    :param location1: The first GPS coordinate
    :type location1: Location
    :param point: The point in the map that the obstacle occupies
    :type point: Numpy Array
    :param uav_bearing: The bearing of the UAV
    :type bearing: float
    """
    dist = float(point[0]**2 + point[1]**2)**0.5 / 1000.1

    lat = location1.get_lat() + (dist * math.cos(uav_bearing) / 111.195)
    lon = location1.get_lon() + ((dist * math.sin(uav_bearing)) / (math.cos(math.radians((lat + location1.get_lat()) / 2.0)) * 111.191))

    return Location(lat, lon, point[2])

def bearing(location1, location2):
    """
    Calculates the bearing between two points

    :param location1: The first GPS location
    :type location1: Location
    :param location2: The second GPS location
    :type location2: Location
    """
    lat1 = math.radians(location1.get_lat())
    lat2 = math.radians(location2.get_lat())
    diffLong = math.radians(location2.get_lon() - location1.get_lat())

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    return initial_bearing
