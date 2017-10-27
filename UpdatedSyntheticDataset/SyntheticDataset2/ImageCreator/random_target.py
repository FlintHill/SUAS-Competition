from PIL import Image
import math
import random
from .settings import Settings
from .specified_target import SpecifiedTarget
from SyntheticDataset2.ElementsCreator.shape_types import ShapeTypes
from SyntheticDataset2.ElementsCreator.shape_orientations import ShapeOrientations

class RandomTarget(object):

    def __init__(self, size_range, proportionality_range, pixelization_level, noise_level):
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
        self.size_range = size_range
        self.proportionality_range = proportionality_range
        self.pixelization_level = pixelization_level
        self.noise_level = noise_level

        shape_type_list = [ShapeTypes.CIRCLE, ShapeTypes.QUARTERCIRCLE, ShapeTypes.HALFCIRCLE,
                           ShapeTypes.CROSS, ShapeTypes.TRIANGLE, ShapeTypes.SQUARE,
                           ShapeTypes.RECTANGLE, ShapeTypes.TRAPEZOID, ShapeTypes.PENTAGON,
                           ShapeTypes.HEXAGON, ShapeTypes.HEPTAGON, ShapeTypes.OCTAGON,
                           ShapeTypes.STAR]
        self.random_shape_type = shape_type_list[random.randint(0, 12)]

        shape_orientation_list = [ShapeOrientations.DIAGONAL, ShapeOrientations.NORTH,
                                  ShapeOrientations.SOUTH, ShapeOrientations.EAST,
                                  ShapeOrientations.WEST, ShapeOrientations.NORTHEAST,
                                  ShapeOrientations.NORTHWEST, ShapeOrientations.SOUTHEAST,
                                  ShapeOrientations.SOUTHWEST, ShapeOrientations.NORTHSOUTH,
                                  ShapeOrientations.EASTWEST]
        if self.random_shape_type == ShapeTypes.CIRCLE:
            self.random_shape_orientation = ShapeOrientations.NORTH
        elif self.random_shape_type == ShapeTypes.QUARTERCIRCLE:
            self.random_shape_orientation = shape_orientation_list[random.randint(1, 8)]
        elif self.random_shape_type == ShapeTypes.HALFCIRCLE:
            self.random_shape_orientation = shape_orientation_list[random.randint(1, 4)]
        elif self.random_shape_type == ShapeTypes.CROSS or self.random_shape_type == ShapeTypes.SQUARE or self.random_shape_type == ShapeTypes.HEXAGON or self.random_shape_type == ShapeTypes.OCTAGON:
            self.random_shape_orientation = shape_orientation_list[random.randint(0, 1)]
        elif self.random_shape_type == ShapeTypes.RECTANGLE:
            self.random_shape_orientation = shape_orientation_list[random.randint(9, 10)]
        else:
            self.random_shape_orientation = shape_orientation_list[random.randint(1, 2)]

        letter_list = ["A", "B", "c", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                       "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        self.random_letter = letter_list[random.randint(0, 25)]

        self.random_size = random.randint(size_range[0], size_range[1])
        self.random_proportionality = random.uniform(proportionality_range[0], proportionality_range[1])

        color_list = [(255, 255, 255, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255),
                      (255, 255, 0, 255), (255, 0, 255, 255), (0, 255, 255, 255), (192, 192, 192, 255), (128, 128, 128, 255),
                      (128, 0, 0, 255), (0, 128, 0, 255), (0, 0, 128, 255), (128, 128, 0, 255), (128, 0, 128, 255),
                      (0, 128, 128, 255)]
        self.random_shape_color = color_list[random.randint(0, 15)]
        color_list.remove(self.random_shape_color)
        self.random_letter_color = color_list[random.randint(0, 14)]

        self.random_rotation = random.randint(0, 180)
        self.pixelization_level = pixelization_level
        self.noise_level = noise_level

    def create_random_target(self):
        """
        Create a random target using SpecifiedTarget with random parameters.
        """
        return SpecifiedTarget(self.random_shape_type, self.random_shape_orientation, self.random_letter, self.random_size, self.random_proportionality, self.random_shape_color, self.random_letter_color, self.random_rotation, self.pixelization_level, self.noise_level).create_specified_target()

    def record_random_target(self):
        text = open(Settings.TEXT_SAVING_PATH + "/tester.txt", "a+")
        text.write("Shape Type: " + str(self.random_shape_type)
                   + "\nAlphanumeric Value: " + str(self.random_letter)
                   + "\nShape Color: " + str(self.random_shape_color)
                   + "\nAlphanumeric Color: " + str(self.random_letter_color)
                   + "\nOrientation: " + str(self.random_rotation))
