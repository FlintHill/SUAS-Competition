from PIL import Image
from .settings import Settings
from .specified_target import SpecifiedTarget
from SyntheticDataset2.ElementsCreator.background import BackgroundGenerator
from SyntheticDataset2.ImageOperations.cardinal_direction_converter import CardinalDirectionConverter
from SyntheticDataset2.logger import Logger

class SpecifiedTargetWithBackground(object):

    def __init__(self, shape_type, shape_orientation, letter, shape_color, letter_color, rotation):
        """
        :param shape_type: the type of the shape to be created.
        :param shape_orientation: the intended orientation of the shape, modified with ShapeOrientator.
        :param letter: the letter to be created.
        :param shape_color: the color of the shape.
        :param letter_color: the color of the letter.
        :param rotation: the intended rotation of the combined image of shape and letter.

        :type shape_type: string (see ShapeTypes)
        :type shape_orientation: string (see ShapeOrientator)
        :type letter: string
        :type shape_color: (R, G, B, A) (:type R, G, B, and A: int from 0 to 255)
        :type letter_color: (R, G, B, A) (:type R, G, B, and A: int from 0 to 255)
        :type rotation: float
        """
        self.shape_type = shape_type
        self.shape_orientation = shape_orientation
        self.letter = letter
        self.shape_color = shape_color
        self.letter_color = letter_color
        self.rotation = rotation

        self.size = Settings.SINGLE_TARGET_SIZE_IN_PIXELS
        self.proportionality = Settings.SINGLE_TARGET_PROPORTIONALITY
        self.pixelization_level = Settings.PIXELIZATION_LEVEL
        self.noise_level = Settings.NOISE_LEVEL

        self.specified_target = SpecifiedTarget(self.shape_type, self.shape_orientation, self.letter, self.size, self.proportionality, self.shape_color, self.letter_color, self.rotation, self.pixelization_level, self.noise_level)

        self.new_target_dimension = Settings.SINGLE_TARGET_SIZE_IN_PIXELS
        self.target_image = self.specified_target.create_specified_target()

        if self.target_image.width >= self.target_image.height:
            self.new_target_width = self.new_target_dimension
            self.new_target_height = self.new_target_dimension * self.target_image.height / self.target_image.width
        else:
            self.new_target_height = self.new_target_dimension
            self.new_target_width = self.new_target_dimension * self.target_image.width / self.target_image.height

    def create_specified_target_with_background(self):
        resized_target_image = self.target_image.resize((self.new_target_width, self.new_target_height))
        self.background = BackgroundGenerator(Settings.BACKGROUND_DIRECTORY).generate_specific_background(resized_target_image.width + 20, resized_target_image.height + 20)
        self.background.paste(resized_target_image, (10, 10), resized_target_image)

        Logger.log("Target's Dimension in pixels: " + str(self.new_target_dimension + 20)
                   + "\nTarget's Dimension in inches: " + str(float(self.new_target_dimension + 20) / Settings.PPSI) + "\n")

        return self.background

    def record_specified_target_with_background(self, file_name):
        data={}
        data["targets"] = []
        data["targets"].append({
            "shape_type": self.shape_type,
            "shape_color": self.shape_color,
            "alphanumeric_value": self.letter,
            "alphanumeric_color": self.letter_color,
            "orientation in degree from north": self.rotation,
            "cardinal orientation": CardinalDirectionConverter.convert_to_cardinal_direction(self.rotation),
            "target_center_coordinates": ((10 + (self.new_target_width / 2)), (10 + (self.new_target_height / 2)))
        })
        with open(Settings.SAVE_PATH + "/single_targets_answers/" + file_name + ".json", 'w') as outfile:
            json.dump(data, outfile, indent=4)

        self.background.save(Settings.SAVE_PATH + "/single_targets/" + file_name + ".jpg")
