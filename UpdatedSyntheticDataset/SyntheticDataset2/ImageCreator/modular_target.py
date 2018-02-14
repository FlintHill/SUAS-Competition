import math
import random
from PIL import Image
from .settings import Settings
from .modular_target_settings import ModularTargetSettings
from .specified_target import SpecifiedTarget
from SyntheticDataset2.ElementsCreator.shape_types import ShapeTypes
from SyntheticDataset2.ElementsCreator.shape_orientations import ShapeOrientations

class ModularTarget(object):

    def __init__(self):
        self.size = Settings.TARGET_GENERATION_SIZE_IN_PIXELS
        self.proportionality_range = Settings.PROPORTIONALITY_RANGE
        self.pixelization_level = Settings.PIXELIZATION_LEVEL
        self.noise_level = Settings.NOISE_LEVEL

        if (ModularTargetSettings.RANDOM_SHAPE_TYPE):
            shape_type_list = [ShapeTypes.CIRCLE, ShapeTypes.QUARTERCIRCLE, ShapeTypes.HALFCIRCLE,
                               ShapeTypes.CROSS, ShapeTypes.TRIANGLE, ShapeTypes.SQUARE,
                               ShapeTypes.RECTANGLE, ShapeTypes.TRAPEZOID, ShapeTypes.PENTAGON,
                               ShapeTypes.HEXAGON, ShapeTypes.HEPTAGON, ShapeTypes.OCTAGON,
                               ShapeTypes.STAR]

            self.shape_type = shape_type_list[random.randint(0, len(shape_type_list) - 1)]

        else:
            self.shape_type = ModularTargetSettings.SHAPE_TYPE

        if (ModularTargetSettings.RANDOM_SHAPE_ORIENTATION):
            shape_orientation_list = [ShapeOrientations.DIAGONAL, ShapeOrientations.NORTH,
                                      ShapeOrientations.SOUTH, ShapeOrientations.EAST,
                                      ShapeOrientations.WEST, ShapeOrientations.NORTHEAST,
                                      ShapeOrientations.NORTHWEST, ShapeOrientations.SOUTHEAST,
                                      ShapeOrientations.SOUTHWEST, ShapeOrientations.NORTHSOUTH,
                                      ShapeOrientations.EASTWEST]

            if self.shape_type == ShapeTypes.CIRCLE:
                self.shape_orientation = ShapeOrientations.NORTH
            elif self.shape_type == ShapeTypes.QUARTERCIRCLE:
                self.shape_orientation = shape_orientation_list[random.randint(1, 8)]
            elif self.shape_type == ShapeTypes.HALFCIRCLE:
                self.shape_orientation = shape_orientation_list[random.randint(1, 4)]
            elif self.shape_type == ShapeTypes.CROSS or self.shape_type == ShapeTypes.SQUARE or self.shape_type == ShapeTypes.HEXAGON or self.shape_type == ShapeTypes.OCTAGON:
                self.shape_orientation = shape_orientation_list[random.randint(0, 1)]
            elif self.shape_type == ShapeTypes.RECTANGLE:
                self.shape_orientation = shape_orientation_list[random.randint(9, 10)]
            else:
                self.shape_orientation = shape_orientation_list[random.randint(1, 2)]

        else:
            self.shape_orientation = ModularTargetSettings.SHAPE_ORIENTATION

        if (ModularTargetSettings.RANDOM_LETTER):
            letter_list = ["A", "B", "c", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                           "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

            self.letter = letter_list[random.randint(0, len(letter_list) - 1)]

        else:
            self.letter = ModularTargetSettings.LETTER

        self.proportionality = random.uniform(self.proportionality_range[0], self.proportionality_range[1])

        color_list = [(255, 255, 255, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255),
                      (128, 128, 128, 255), (255, 255, 0, 255), (255, 165, 0, 255), (128, 0, 128, 255), (165, 42, 42, 255)]

        if (ModularTargetSettings.RANDOM_SHAPE_COLOR):
            self.shape_color = color_list[random.randint(0, len(color_list) - 1)]
            while (self.shape_color == (0, 0, 0, 255)):
                self.shape_color = color_list[random.randint(0, len(color_list) - 1)]
            color_list.remove(self.shape_color)

        else:
            self.shape_color = ModularTargetSettings.SHAPE_COLOR

        if (ModularTargetSettings.RANDOM_LETTER_COLOR):
            self.letter_color = color_list[random.randint(0, len(color_list) - 1)]

        else:
            self.letter_color = ModularTargetSettings.LETTER_COLOR

        self.rotation = random.uniform(0.0, 360.0)

    def create_modular_target(self):
        """
        Create a modular target using SpecifiedTarget.
        """
        return SpecifiedTarget(self.shape_type, self.shape_orientation, self.letter, self.size, self.proportionality, self.shape_color, self.letter_color, self.rotation, self.pixelization_level, self.noise_level).create_specified_target()
