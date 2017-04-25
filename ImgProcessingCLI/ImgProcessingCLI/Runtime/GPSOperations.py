import numpy
from math import cos, sin, atan2, radians

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

def get_bearing(base_xy, end_xy):
    return atan2(end_xy[1]-base_xy[1], end_xy[0]-base_xy[0])
