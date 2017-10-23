from PIL import Image
import math
import random
from SyntheticDataset2.ElementsCreator import *
from SyntheticDataset2.ImageOperations.shape_orientator import ShapeOrientator
from SyntheticDataset2.ImageOperations.bounded_image_cropper import BoundedImageCropper
from SyntheticDataset2.ImageOperations.image_paster import ImagePaster
from .specified_target_creator import SpecifiedTargetCreator

class RandomTargetCreator(object):

    @staticmethod
    def create_random_target(size_range, proportionality_range):
        """
        Create a random target using SpecifiedTargetCreator with random parameters.
        :param size_range: the range of sizes that are to be selected randomly
        :param proportionality_range: the range of proportionality levels that are to be selected randomly
        :type size_range: [min_size, max_size] //:type min_size and max_size: int
        :type proportionality_range: [min_proportionality, max_proportionality] //:type min_proportionality and max_proportionality: double
        """
        shape_type_list = [ShapeTypes.CIRCLE, ShapeTypes.QUARTERCIRCLE, ShapeTypes.HALFCIRCLE,
                           ShapeTypes.CROSS, ShapeTypes.TRIANGLE, ShapeTypes.SQUARE,
                           ShapeTypes.RECTANGLE, ShapeTypes.TRAPEZOID, ShapeTypes.PENTAGON,
                           ShapeTypes.HEXAGON, ShapeTypes.HEPTAGON, ShapeTypes.OCTAGON,
                           ShapeTypes.STAR]

        shape_orientation_list = [ShapeOrientations.DIAGONAL, ShapeOrientations.NORTH,
                                  ShapeOrientations.SOUTH, ShapeOrientations.EAST,
                                  ShapeOrientations.WEST, ShapeOrientations.NORTHEAST,
                                  ShapeOrientations.NORTHWEST, ShapeOrientations.SOUTHEAST,
                                  ShapeOrientations.SOUTHWEST, ShapeOrientations.NORTHSOUTH,
                                  ShapeOrientations.EASTWEST]

        random_shape_type = shape_type_list[random.randint(0, 12)]

        if random_shape_type == ShapeTypes.CIRCLE:
            random_shape_orientation = ShapeOrientations.NORTH

        elif random_shape_type == ShapeTypes.QUARTERCIRCLE:
            random_shape_orientation = shape_orientation_list[random.randint(1, 8)]

        elif random_shape_type == ShapeTypes.HALFCIRCLE:

            random_shape_orientation = shape_orientation_list[random.randint(1, 4)]

        elif random_shape_type == ShapeTypes.CROSS or random_shape_type == ShapeTypes.SQUARE or random_shape_type == ShapeTypes.HEXAGON or random_shape_type == ShapeTypes.OCTAGON:
            random_shape_orientation = shape_orientation_list[random.randint(0, 1)]

        elif random_shape_type == ShapeTypes.RECTANGLE:
            random_shape_orientation = shape_orientation_list[random.randint(9, 10)]

        else:
            random_shape_orientation = shape_orientation_list[random.randint(1, 2)]

        random_color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256), 255)
        color_list = [(255, 255, 255, 255), (0, 0, 0, 255), (255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255),
                      (255, 255, 0, 255), (255, 0, 255, 255), (0, 255, 255, 255), random_color]
        random_color1 = color_list[random.randint(0, 8)]
        color_list.remove(random_color1)
        random_color2 = color_list[random.randint(0, 7)]

        letter_list = ["A", "B", "c", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                       "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        random_letter = letter_list[random.randint(0, 25)]

        random_size = random.randint(size_range[0], size_range[1])

        random_proportionality = random.uniform(proportionality_range[0], proportionality_range[1])

        random_rotation = random.randint(0, 180)

        return SpecifiedTargetCreator.create_specified_target(random_shape_type, random_shape_orientation, random_letter, random_size, random_proportionality, random_color1, random_color2, random_rotation)
