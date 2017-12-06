from PIL import Image
import math, random, json
from .settings import Settings
from .specified_target import SpecifiedTarget
from SyntheticDataset2.ElementsCreator.shape_types import ShapeTypes
from SyntheticDataset2.ElementsCreator.shape_orientations import ShapeOrientations

class RandomTarget(object):

    def __init__(self, shape_type, shape_orientation, letter, size_range, proportionality_range, shape_color, letter_color, rotation, pixelization_level, noise_level):
        """
        :param size_range: the range of sizes that are to be selected randomly
        :param proportionality_range: the range of proportionality levels that are to be selected randomly
        :param pixelization_level: the level of pixelization, see the first method of ImageResizer
        :param noise_level: the intended level of noise. (See gaussian_noise_generator for detail.)

        :type size_range: [min_size, max_size] //:type min_size and max_size: int
        :type proportionality_range: [min_proportionality, max_proportionality] //:type min_proportionality and max_proportionality: double
        :type pixelization_level: float (preferably below 20.0)
        :type noise_level: float (0.0 to 100.0)
        """
        self.shape_type = shape_type
        self.shape_orientation = shape_orientation
        self.letter = letter
        self.size_range = size_range
        self.proportionality_range = proportionality_range
        self.shape_color = shape_color
        self.letter_color = letter_color
        self.rotaton = rotation
        self.pixelization_level = pixelization_level
        self.noise_level = noise_level

        shape_type_list = [ShapeTypes.CIRCLE, ShapeTypes.QUARTERCIRCLE, ShapeTypes.HALFCIRCLE,
                           ShapeTypes.CROSS, ShapeTypes.TRIANGLE, ShapeTypes.SQUARE,
                           ShapeTypes.RECTANGLE, ShapeTypes.TRAPEZOID, ShapeTypes.PENTAGON,
                           ShapeTypes.HEXAGON, ShapeTypes.HEPTAGON, ShapeTypes.OCTAGON,
                           ShapeTypes.STAR]

        if (self.shape_type == "randomize"):
            self.shape_type = shape_type_list[random.randint(0, 12)]

        shape_orientation_list = [ShapeOrientations.DIAGONAL, ShapeOrientations.NORTH,
                                  ShapeOrientations.SOUTH, ShapeOrientations.EAST,
                                  ShapeOrientations.WEST, ShapeOrientations.NORTHEAST,
                                  ShapeOrientations.NORTHWEST, ShapeOrientations.SOUTHEAST,
                                  ShapeOrientations.SOUTHWEST, ShapeOrientations.NORTHSOUTH,
                                  ShapeOrientations.EASTWEST]

        if (self.shape_type == "randomize"):
            if self.shape_type == ShapeTypes.CIRCLE:
                self.shape_orientation = ShapeOrientations.NORTH
            elif self.shape_type == ShapeTypes.QUARTERCIRCLE:
                self.shape_orientation = shape_orientation_list[random.randint(1, 8)]
            elif self.shape_type == ShapeTypes.HALFCIRCLE:
                self.shape_orientation = shape_orientation_list[random.randint(1, 4)]
            elif self.shape_type == ShapeTypes.CROSS or self.random_shape_type == ShapeTypes.SQUARE or self.random_shape_type == ShapeTypes.HEXAGON or self.random_shape_type == ShapeTypes.OCTAGON:
                self.shape_orientation = shape_orientation_list[random.randint(0, 1)]
            elif self.shape_type == ShapeTypes.RECTANGLE:
                self.shape_orientation = shape_orientation_list[random.randint(9, 10)]
            else:
                self.shape_orientation = shape_orientation_list[random.randint(1, 2)]

        letter_list = ["A", "B", "c", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                       "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

        if (self.letter == "randomize"):
            self.letter = letter_list[random.randint(0, 25)]

        self.size = random.randint(size_range[0], size_range[1])

        self.proportionality = random.uniform(proportionality_range[0], proportionality_range[1])

        color_list = [(255, 255, 255, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255),
                      (128, 128, 128, 255), (255, 255, 0, 255), (255, 165, 0, 255), (128, 0, 128, 255), (165, 42, 42, 255)]

        if (self.shape_color == "randomize"):
            self.shape_color = color_list[random.randint(0, 9)]
            color_list.remove(self.shape_color)

            if (self.letter_color == "randomize"):
                self.letter_color = color_list[random.randint(0, 8)]

        if (self.letter_color == "randomize"):
            self.letter_color = color_list[random.randint(0, 9)]

        self.rotation = random.uniform(0.0, 360.0)
        self.pixelization_level = pixelization_level
        self.noise_level = noise_level

    def create_random_target(self):
        """
        Create a random target using SpecifiedTarget with random parameters.
        """
        return SpecifiedTarget(self.shape_type, self.shape_orientation, self.letter, self.size, self.proportionality, self.shape_color, self.letter_color, self.rotation, self.pixelization_level, self.noise_level).create_specified_target()
