from PIL import Image
import math
from SyntheticDataset2.ElementsCreator import *
from SyntheticDataset2.ImageOperations import *

class TargetCreator(object):

    @staticmethod
    def create_specified_single_target(shape_type, shape_orientation, letter, size, proportionality, shape_color, letter_color):
        """
        :param shape_type: the type of the shape intended to create.
        :param shape_orientation: the intended orientation of the shape, modified with ShapeOrientator.
        :param letter: the letter intended to create.
        :param size: a parameter of the sizes of the shapes. Different shapes have different ways to use "size"
                     (for circles, "size" = radius; for squares, "size" = side length, etc.)
        :param proportionality: a parameter of the proportionality between the shapes and the letters.
                                "proportionality" is a value, not a specific proportionality between the
                                dimensions of the shapes and letters as different shapes fit differently with
                                the letters. 2 is the ideal value of "proportionality". Increasing
                                "proportionality" decreases the size of the letter while the size of the shape
                                stays constant.
        :param shape_color: the intended color of the shape.
        :param letter_color: the intended color of the letter.
        :type shape_type: string (see ShapeTypes)
        :type shape_orientation: string (see ShapeOrientator)
        :type letter: string
        :type size: an int (representing pixel)
        :type proportionality: float
        :type shape_color: (R, G, B, A)
        :type letter_color: (R, G, B, A)
        :type R, G, B, and A: int from 0 to 255
        """

        font_type = "UpdatedSyntheticDataset/data/fonts/Blockletter.otf"

        if shape_type == ShapeTypes.CIRCLE:
            shape_image = Circle(size / 2, shape_color).draw()

        if shape_type == ShapeTypes.QUARTERCIRCLE:
            shape_image = QuarterCircle(size, shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        if shape_type == ShapeTypes.HALFCIRCLE:
            shape_image = HalfCircle(size, shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        if shape_type == ShapeTypes.CROSS:
            shape_image = Cross(int(size * 1.5), shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        if shape_type == ShapeTypes.TRIANGLE:
            shape_image = Triangle(int(size * 1.5), int(size * 1.5 / 2 * math.sqrt(3)), shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        if shape_type == ShapeTypes.SQUARE:
            shape_image = Square(size / 2, shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        if shape_type == ShapeTypes.RECTANGLE:
            shape_image = Rectangle(size / 2, int(size * 0.75), shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        if shape_type == ShapeTypes.TRAPEZOID:
            shape_image = Trapezoid(size / 2, size, size / 2, shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        if shape_type == ShapeTypes.PENTAGON:
            shape_image = Pentagon(size / 2, shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        if shape_type == ShapeTypes.HEXAGON:
            shape_image = Hexagon(size / 2, shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        if shape_type == ShapeTypes.HEPTAGON:
            shape_image = Heptagon(size / 2, shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        if shape_type == ShapeTypes.OCTAGON:
            shape_image = Octagon(size / 2, shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        if shape_type == ShapeTypes.STAR:
            shape_image = Star(int(size / 2), shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        cropped_shape_image = BoundedImageCropper.crop_bounded_image(shape_image, shape_image.load(), shape_color)
        letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0) / proportionality), letter_color).generate_specified_letter()

        if shape_type == ShapeTypes.TRIANGLE:
            if shape_orientation == "N":
                return ImagePaster.paste_images_triangle_angle_north(cropped_shape_image, letter_image)

            if shape_orientation == "S":
                return ImagePaster.paste_images_triangle_angle_south(cropped_shape_image, letter_image)

        if shape_type == ShapeTypes.PENTAGON or shape_type == ShapeTypes.STAR:
            if shape_orientation == "N":
                return ImagePaster.paste_images_pentagon_angle_north(cropped_shape_image, letter_image)

            if shape_orientation == "S":
                return ImagePaster.paste_images_pentagon_angle_south(cropped_shape_image, letter_image)

        if shape_type == ShapeTypes.QUARTERCIRCLE:
            if shape_orientation == "NE":
                return ImagePaster.paste_images_quarter_circle_northeast(cropped_shape_image, letter_image)

            if shape_orientation == "SE":
                return ImagePaster.paste_images_quarter_circle_southeast(cropped_shape_image, letter_image)

            if shape_orientation == "SW":
                return ImagePaster.paste_images_quarter_circle_southwest(cropped_shape_image, letter_image)

            if shape_orientation == "NW":
                return ImagePaster.paste_images_quarter_circle_northwest(cropped_shape_image, letter_image)

            else:
                return ImagePaster.paste_images(cropped_shape_image, letter_image)

        else:
            return ImagePaster.paste_images(cropped_shape_image, letter_image)
