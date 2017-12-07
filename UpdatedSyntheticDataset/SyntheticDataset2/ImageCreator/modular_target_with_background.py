from PIL import Image
import random, json
from .settings import Settings
from .modular_target import ModularTarget
from SyntheticDataset2.ElementsCreator.background import BackgroundGenerator
from SyntheticDataset2.ElementsCreator.raw_image_generator import RawImageGenerator
from SyntheticDataset2.ImageOperations.cardinal_direction_converter import CardinalDirectionConverter
from SyntheticDataset2.logger import Logger

class ModularTargetWithBackground(object):

    def __init__(self):
        self.modular_target = ModularTarget()

        self.new_target_dimension = random.randint(Settings.TARGET_SIZE_RANGE_IN_PIXELS[0], Settings.TARGET_SIZE_RANGE_IN_PIXELS[1])
        self.target_image = self.modular_target.create_modular_target()

        if self.target_image.width >= self.target_image.height:
            self.new_target_width = self.new_target_dimension
            self.new_target_height = self.new_target_dimension * self.target_image.height / self.target_image.width
        else:
            self.new_target_height = self.new_target_dimension
            self.new_target_width = self.new_target_dimension * self.target_image.width / self.target_image.height

    def create_modular_target_with_background(self):
        resized_target_image = self.target_image.resize((self.new_target_width, self.new_target_height))

        if (Settings.CREATE_SYNTHETIC_BACKGROUND):
            self.background = BackgroundGenerator(Settings.BACKGROUND_DIRECTORY_PATH).generate_specific_background(resized_target_image.width + 20, resized_target_image.height + 20)

        else:
            self.background = RawImageGenerator.generate_raw_image(resized_target_image.width + 20, resized_target_image.height + 20, (255, 255, 255, 0))

        self.background.paste(resized_target_image, (10, 10), resized_target_image)

        Logger.log("Target's Dimension in pixels: " + str(self.new_target_dimension + 20)
                   + "\nTarget's Dimension in inches: " + str(float(self.new_target_dimension + 20) / Settings.PPSI)
                   + "\nshape_type: " + self.modular_target.shape_type
                   + "\nshape_color: (" + str(self.modular_target.shape_color[0]) + ", " + str(self.modular_target.shape_color[1]) + ", " + str(self.modular_target.shape_color[2]) + ")"
                   + "\nalphanumeric_value: " + self.modular_target.letter
                   + "\nalphanumeric_color: (" + str(self.modular_target.letter_color[0]) + ", " + str(self.modular_target.letter_color[1]) + ", " + str(self.modular_target.letter_color[2]) + ")"
                   + "\norientation in degree from north: " + str(self.modular_target.rotation)
                   + "\ncardinal orientation: " + CardinalDirectionConverter.convert_to_cardinal_direction(self.modular_target.rotation)
                   + "\ntarget_center_coordinates: " + str(10+(self.new_target_width / 2)) + ", " + str(10 + (self.new_target_height / 2)) + "\n")

        return self.background

    def record_modular_target_with_background(self, index_number):
        data={}
        data["targets"] = []
        data["targets"].append({
            "shape_type": self.modular_target.shape_type,
            "shape_color": self.modular_target.shape_color,
            "alphanumeric_value": self.modular_target.letter,
            "alphanumeric_color": self.modular_target.letter_color,
            "orientation in degree from north": self.modular_target.rotation,
            "cardinal orientation": CardinalDirectionConverter.convert_to_cardinal_direction(self.modular_target.rotation),
            "target_center_coordinates": ((10+(self.new_target_width / 2)), (10 + (self.new_target_height / 2)))
        })
        with open(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/modular_single_targets_with_background_answers/" + str(index_number) + ".json", 'w') as outfile:
            json.dump(data, outfile, indent=4)

        self.background.save(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/modular_single_targets_with_background/" + str(index_number) + ".png")
