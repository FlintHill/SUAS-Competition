from math import radians, cos, sin, asin, sqrt

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

def bearing(gps1, gps2):
    bearing = atan2(sin(gps2.get_longitude()-gps1.get_longitude())*cos(gps2.get_longitude()), cos(gps1.get_latitude())*sin(lat2)-sin(gps1.get_latitude())*cos(gps2.get_latitude())*cos(gps2.get_longitude()-gps1.get_longitude()))
    #bearing = degrees(bearing)
    #bearing = (bearing + 360) % 360

    return bearing
