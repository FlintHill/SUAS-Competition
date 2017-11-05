from PIL import Image
import random, json
from .settings import Settings
from .random_target import RandomTarget
from SyntheticDataset2.ElementsCreator.background import BackgroundGenerator
from SyntheticDataset2.ImageOperations.cardinal_direction_converter import CardinalDirectionConverter
from SyntheticDataset2.logger import Logger

class RandomTargetWithBackground(object):

    def __init__(self):
        self.size_range = Settings.TARGET_SIZE_RANGE_IN_PIXELS
        self.proportionality_range = Settings.PROPORTIONALITY_RANGE
        self.pixelization_level = Settings.PIXELIZATION_LEVEL
        self.noise_level = Settings.NOISE_LEVEL

        self.random_target = RandomTarget(self.size_range, self.proportionality_range, self.pixelization_level, self.noise_level)

        self.new_target_dimension = random.randint(Settings.TARGET_SIZE_RANGE_IN_PIXELS[0], Settings.TARGET_SIZE_RANGE_IN_PIXELS[1])
        self.target_image = self.random_target.create_random_target()

        if self.target_image.width >= self.target_image.height:
            self.new_target_width = self.new_target_dimension
            self.new_target_height = self.new_target_dimension * self.target_image.height / self.target_image.width
        else:
            self.new_target_height = self.new_target_dimension
            self.new_target_width = self.new_target_dimension * self.target_image.width / self.target_image.height

    def create_random_target_with_background(self):
        resized_target_image = self.target_image.resize((self.new_target_width, self.new_target_height))
        self.background = BackgroundGenerator(Settings.BACKGROUND_DIRECTORY_PATH).generate_specific_background(resized_target_image.width + 20, resized_target_image.height + 20)
        self.background.paste(resized_target_image, (10, 10), resized_target_image)

        Logger.log("Target's Dimension in pixels: " + str(self.new_target_dimension + 20)
                   + "\nTarget's Dimension in inches: " + str(float(self.new_target_dimension + 20) / Settings.PPSI)
                   + "\nshape_type: " + self.random_target.random_shape_type
                   + "\nshape_color: (" + str(self.random_target.random_shape_color[0]) + ", " + str(self.random_target.random_shape_color[1]) + ", " + str(self.random_target.random_shape_color[2]) + ")"
                   + "\nalphanumeric_value: " + self.random_target.random_letter
                   + "\nalphanumeric_color: (" + str(self.random_target.random_letter_color[0]) + ", " + str(self.random_target.random_letter_color[1]) + ", " + str(self.random_target.random_letter_color[2]) + ")"
                   + "\norientation in degree from north: " + str(self.random_target.random_rotation)
                   + "\ncardinal orientation: " + CardinalDirectionConverter.convert_to_cardinal_direction(self.random_target.random_rotation)
                   + "\ntarget_center_coordinates: " + str(10+(self.new_target_width / 2)) + ", " + str(10 + (self.new_target_height / 2)) + "\n")

        return self.background

    def record_random_target_with_background(self, index_number):
        data={}
        data["targets"] = []
        data["targets"].append({
            "shape_type": self.random_target.random_shape_type,
            "shape_color": self.random_target.random_shape_color,
            "alphanumeric_value": self.random_target.random_letter,
            "alphanumeric_color": self.random_target.random_letter_color,
            "orientation in degree from north": self.random_target.random_rotation,
            "cardinal orientation": CardinalDirectionConverter.convert_to_cardinal_direction(self.random_target.random_rotation),
            "target_center_coordinates": ((10+(self.new_target_width / 2)), (10 + (self.new_target_height / 2)))
        })
        with open(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/single_targets_answers/" + str(index_number) + ".json", 'w') as outfile:
            json.dump(data, outfile, indent=4)

        self.background.save(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/single_targets/" + str(index_number) + ".jpg")
