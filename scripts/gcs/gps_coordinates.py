from abc import ABCMeta
import math

class GPSCoordinates:

    __metaclass__ = ABCMeta

    def __init__(self, lat, lon, alt):
        self.lat = lat
        self.lon = lon
        self.alt = alt

    def get_altitude(self):
        return self.alt

    def get_longitude(self):
        return self.lon

    def get_longitude_radians(self):
        return math.radians(self.lon)

    def get_latitude(self):
        return self.lat

    def get_latitude_radians(self):
        return math.radians(self.lat)
