
class GeoStamp(object):
    def __init__(self, geo_pos, time_stamp):
        self.geo_pos = geo_pos
        self.time_stamp = time_stamp

    def get_geo(self):
        return self.geo_pos

    def get_time_stamp(self):
        return self.time_stamp
