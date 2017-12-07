from PIL import Image
import math, random, json
from .settings import Settings
from .specified_target import SpecifiedTarget
from SyntheticDataset2.ElementsCreator.shape_types import ShapeTypes
from SyntheticDataset2.ElementsCreator.shape_orientations import ShapeOrientations

class RandomTarget(object):

    def __init__(self):
        self.size = Settings.TARGET_GENERATION_SIZE_IN_PIXELS
        self.proportionality_range = Settings.PROPORTIONALITY_RANGE
        self.pixelization_level = Settings.PIXELIZATION_LEVEL
        self.noise_level = Settings.NOISE_LEVEL

        shape_type_list = [ShapeTypes.CIRCLE, ShapeTypes.QUARTERCIRCLE, ShapeTypes.HALFCIRCLE,
                           ShapeTypes.CROSS, ShapeTypes.TRIANGLE, ShapeTypes.SQUARE,
                           ShapeTypes.RECTANGLE, ShapeTypes.TRAPEZOID, ShapeTypes.PENTAGON,
                           ShapeTypes.HEXAGON, ShapeTypes.HEPTAGON, ShapeTypes.OCTAGON,
                           ShapeTypes.STAR]

        self.shape_type = shape_type_list[random.randint(0, 12)]

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

        letter_list = ["A", "B", "c", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                       "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

        self.letter = letter_list[random.randint(0, 25)]

        self.proportionality = random.uniform(self.proportionality_range[0], self.proportionality_range[1])

        color_list = [(255, 255, 255, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255),
                      (128, 128, 128, 255), (255, 255, 0, 255), (255, 165, 0, 255), (128, 0, 128, 255), (165, 42, 42, 255)]

        self.shape_color = color_list[random.randint(0, 9)]
        color_list.remove(self.shape_color)

        self.letter_color = color_list[random.randint(0, 8)]

        self.rotation = random.uniform(0.0, 360.0)

    def create_random_target(self):
        """
        Create a random target using SpecifiedTarget with random parameters.
        """
        return SpecifiedTarget(self.shape_type, self.shape_orientation, self.letter, self.size, self.proportionality, self.shape_color, self.letter_color, self.rotation, self.pixelization_level, self.noise_level).create_specified_target()
