from PIL import Image
import random, json
from .settings import Settings
from .random_target import RandomTarget
from SyntheticDataset2.ElementsCreator.raw_image_generator import RawImageGenerator
from SyntheticDataset2.ImageOperations.cardinal_direction_converter import CardinalDirectionConverter
from SyntheticDataset2.logger import Logger

class RandomTargetWithoutBackground(object):

    def __init__(self):
        self.random_target = RandomTarget()

        self.new_target_dimension = random.randint(Settings.TARGET_SIZE_RANGE_IN_PIXELS[0], Settings.TARGET_SIZE_RANGE_IN_PIXELS[1])
        self.target_image = self.random_target.create_random_target()

        if self.target_image.width >= self.target_image.height:
            self.new_target_width = self.new_target_dimension
            self.new_target_height = self.new_target_dimension * self.target_image.height / self.target_image.width
        else:
            self.new_target_height = self.new_target_dimension
            self.new_target_width = self.new_target_dimension * self.target_image.width / self.target_image.height

    def create_random_target_without_background(self):
        resized_target_image = self.target_image.resize((self.new_target_width, self.new_target_height))
        self.background = RawImageGenerator.generate_raw_image(resized_target_image.width + 20, resized_target_image.height + 20, (255, 255, 255, 0))
        self.background.paste(resized_target_image, (10, 10), resized_target_image)

        Logger.log("Target's Dimension in pixels: " + str(self.new_target_dimension + 20)
                   + "\nTarget's Dimension in inches: " + str(float(self.new_target_dimension + 20) / Settings.PPSI)
                   + "\nshape_type: " + self.random_target.shape_type
                   + "\nshape_color: (" + str(self.random_target.shape_color[0]) + ", " + str(self.random_target.shape_color[1]) + ", " + str(self.random_target.shape_color[2]) + ")"
                   + "\nalphanumeric_value: " + self.random_target.letter
                   + "\nalphanumeric_color: (" + str(self.random_target.letter_color[0]) + ", " + str(self.random_target.letter_color[1]) + ", " + str(self.random_target.letter_color[2]) + ")"
                   + "\norientation in degree from north: " + str(self.random_target.rotation)
                   + "\ncardinal orientation: " + CardinalDirectionConverter.convert_to_cardinal_direction(self.random_target.rotation)
                   + "\ntarget_center_coordinates: " + str(10+(self.new_target_width / 2)) + ", " + str(10 + (self.new_target_height / 2)) + "\n")

        return self.background

    def record_random_target_without_background(self, index_number):
        data={}
        data["targets"] = []
        data["targets"].append({
            "shape_type": self.random_target.shape_type,
            "shape_color": self.random_target.shape_color,
            "alphanumeric_value": self.random_target.letter,
            "alphanumeric_color": self.random_target.letter_color,
            "orientation in degree from north": self.random_target.rotation,
            "cardinal orientation": CardinalDirectionConverter.convert_to_cardinal_direction(self.random_target.rotation),
            "target_center_coordinates": ((10+(self.new_target_width / 2)), (10 + (self.new_target_height / 2)))
        })
        with open(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/random_single_targets_without_background_answers/" + str(index_number) + ".json", 'w') as outfile:
            json.dump(data, outfile, indent=4)

        self.background.save(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/random_single_targets_without_background/" + str(index_number) + ".png")
