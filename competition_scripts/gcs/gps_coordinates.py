from abc import ABCMeta

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

    def get_latitude(self):
        return self.lat
