import numpy
from math import cos, sin, atan2, radians, pi


EARTH_RADIUS_KM = 6371.0
EQUITORIAL_EARTH_RADIUS_KM = 6378.1370

def inverse_haversine(base_xy, end_xy, base_geo):
    '''
    takes the cartesian coordinates base_xy and end_xy, where end_xy is the coordinate position of the object to which you are measuring,
    and base_xy is cartesian coordinate linked to the gps coordinate base_geo. base_xy and end_xy are in feet
    '''
    point_bearing = get_bearing(base_xy, end_xy)
    dist = numpy.linalg.norm(base_xy - end_xy)*0.0003048

    d_lat = base_geo[0] + (dist * cos(point_bearing) / 111.195)
    d_long = base_geo[1] + ((dist * sin(point_bearing)) / (cos(radians((d_lat + base_geo[0]) / 2.0)) * 111.191))

    return (d_lat, d_long)

def haversine_distance(lat_lon1, lat_lon2):
    lat_lon1_radians = 180.0 * numpy.array(lat_lon1)/pi
    lat_lon2_radians = 180.0 * numpy.array(lat_lon2)/pi
    dlon = lat_lon2_radians[0] - lat_lon1_radians[0]
    dlat = lat_lon2_radians[1] - lat_lon1_radians[1]
    
    a = (sin(dlat/2))**2 + cos(lat_lon1_radians[0]) * cos(lat_lon2_radians[0]) * (sin(dlon/2))**2
    c = 2.0 * atan2( sqrt(a), sqrt(1-a) )
    geo_dist = EARTH_RADIUS_KM * c

    return geo_dist

def get_bearing(base_xy, end_xy):
    return atan2(end_xy[1]-base_xy[1], end_xy[0]-base_xy[0])
