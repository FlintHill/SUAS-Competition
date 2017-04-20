from ImgProcessingCLI.General.TargetTwo import TargetTwo
import ImgProcessingCLI.Runtime.TimeOps as TimeOps
from ImgProcessingCLI.Runtime.GeoStamp import GeoStamp

class RuntimeTarget(object):
    def __init__(self, crop_dy_dx, time_taken, target_img, letter_categorizer, orientation_solver, geo_stamps, time_first_img_taken):
        self.letter_categorizer = letter_categorizer
        self.orientation_solver = orientation_solver
        self.target_img = target_img
        self.init_target_obj()
        self.set_target_traits()
        self.init_time_img_taken(time_taken, time_first_img_taken)
        self.init_target_geo_stamp(geo_stamps)
        self.init_target_geolocation(crop_dy_dx)

    def init_target_obj(self):
        self.target_obj = TargetTwo(self.target_img.convert('RGB'), self.target_img.convert('RGB').load(), self.letter_categorizer, self.orientation_solver)

    def set_target_traits(self):
        '''needs to be converted to JSON'''
        self.target_characteristics = self.target_obj.as_numpy()
        print("target characteristics: ", self.target_characteristics)

    def init_time_img_taken(self, time_taken, time_first_img_taken):

        self.second_taken = time_taken - time_first_img_taken
        print("second taken: ", self.second_taken)

    def init_target_geo_stamp(self, geo_stamps):
        self.target_geo_stamp = geo_stamps.get_closest_geo_stamp_to_time(self.second_taken)

    def init_target_geolocation(self, crop_dy_dx):
        '''needs to use reverse haversine and PPSI to find the geolocation of the target within the image.
        For now will just return the geolocation of the stamp of the image'''
        self.target_geolocation = self.target_geo_stamp.get_geo()

    def get_crop(self):
        return self.target_img
