from ImgProcessingCLI.General.TargetTwo import TargetTwo
from ImgProcessingCLI.Runtime.GeoStamp import GeoStamp
import json

class RuntimeTarget(TargetTwo):

    def __init__(self, target_crop, letter_categorizer_in, orientation_solver_in, standard_target=True):
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
