from ImgProcessingCLI.General.TargetTwo import TargetTwo
import ImgProcessingCLI.Runtime.TimeOps as TimeOps
from ImgProcessingCLI.Runtime.GeoStamp import GeoStamp
import json

class RuntimeTarget(TargetTwo):

    def __init__(self, target_crop, letter_categorizer_in, orientation_solver_in, standard_target = True):
        crop_img = target_crop.get_crop_img()
        TargetTwo.__init__(self, crop_img, crop_img.load(), letter_categorizer_in, orientation_solver_in)
        self.target_crop = target_crop
        self.set_competition_json_output(standard_target)



    def set_competition_json_output(self, standard_target):
        loaded_target_two_json = json.loads(self.as_json())
        json_out_temp = {
        "type": "standard" if standard_target else "emergent",
        "latitude": self.target_crop.get_crop_gps_lat_lon()[0],
        "longitude": self.target_crop.get_crop_gps_lat_lon()[1],
        "orientation": loaded_target_two_json["orientation"].lower(),
        "shape": loaded_target_two_json["shape"],
        "background_color": loaded_target_two_json["background_color"],
        "alphanumeric": loaded_target_two_json["alphanumeric"],
        "alphanumeric_color": loaded_target_two_json["alphanumeric_color"]}

        self.competition_json_output = json.dumps(json_out_temp)

    def get_competition_json_output(self):
        return self.competition_json_output


    '''
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

        self.target_characteristics = self.target_obj.as_numpy()
        print("target characteristics: ", self.target_characteristics)

    def init_time_img_taken(self, time_taken, time_first_img_taken):

        self.second_taken = time_taken - time_first_img_taken
        print("second taken: ", self.second_taken)

    def init_target_geo_stamp(self, geo_stamps):
        self.target_geo_stamp = geo_stamps.get_closest_geo_stamp_to_time(self.second_taken)

    def init_target_geolocation(self, crop_dy_dx):

    def get_crop(self):
        return self.target_img
    '''
