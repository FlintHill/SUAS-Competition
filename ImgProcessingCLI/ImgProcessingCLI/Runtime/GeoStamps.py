

class GeoStamps(object):
    def __init__(self, geo_stamps):
        self.geo_stamps = geo_stamps

    def get_closest_geo_stamp_to_second(self, time):
        sorted_geo_stamps = sorted(self.geo_stamps, key = lambda stamp: int((stamp.get_time_stamp() - time).total_seconds()))
        return sorted_geo_stamps[0]
