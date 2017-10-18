from PIL import Image
import math
from SyntheticDataset2.ElementsCreator import *
from SyntheticDataset2.ImageOperations import *

class TargetCreator(object):
    """
    :param shapelist: the list of shapes that are going to be used. Orientations are separated.
        indexes:
        0 = circle

        1 = quarter circle with corner facing up
        2 = quarter circle with corner facing up right
        3 = quarter circle with corner facing right
        4 = quarter circle with corner facing down right
        5 = quarter circle with corner facing down
        6 = quarter circle with corner facing down left
        7 = quarter circle with corner facing left
        8 = quarter circle with corner facing up left

        9 = half circle with side facing up
        10 = half circle with side facing right
        11 = half circle with side facing down
        12 = half circle with side facing left

        13 = cross with convex facing up
        14 = cross with concave facing up

        15 = triangle with angle facing up
        16 = triangle with side facing up

        17 = square with angle facing up
        18 = square with side facing up

        19 = rectangle with shorter side facing up
        20 = rectangle with longer side facing up

        21 = trapezoid with shorter side facing up
        22 = trapezoid with longer side facing up

        23 = pentagon with angle facing up
        24 = pentagon with side facing up

        25 = hexagon with angle facing up
        26 = hexagon with side facing up

        27 = heptagon with angle facing up
        28 = heptagon with side facing up

        29 = octagon with angle facing up
        30 = octagon with side facing up

        31 = star with convex facing up
        32 = star with concave facing up
    """

    @staticmethod
    def create_specified_single_target(shape_index, letter, size, proportionality, shape_color, letter_color):
        """
        :param shape_index: the index of the shape intended to create. The indexes are listed above.
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
        :type shape_index: an int from 0 to 32 (inclusive)
        :type letter: string
        :type size: an int (representing pixel)
        :type proportionality: float
        :type shape_color: (R, G, B, A)
        :type letter_color: (R, G, B, A)
        :type R, G, B, and A: int from 0 to 255
        """
        font_type = "UpdatedSyntheticDataset/data/fonts/Blockletter.otf"
        if shape_index == 0:
            shape_image = Circle(size / 2, shape_color).draw()

        if shape_index == 1:
            shape_image = QuarterCircle(size, shape_color, 135).draw()

        if shape_index == 2:
            shape_image = QuarterCircle(size, shape_color, 90).draw()

        if shape_index == 3:
            shape_image = QuarterCircle(size, shape_color, 45).draw()

        if shape_index == 4:
            shape_image = QuarterCircle(size, shape_color, 0).draw()

        if shape_index == 5:
            shape_image = QuarterCircle(size, shape_color, -45).draw()

        if shape_index == 6:
            shape_image = QuarterCircle(size, shape_color, -90).draw()

        if shape_index == 7:
            shape_image = QuarterCircle(size, shape_color, -135).draw()

        if shape_index == 8:
            shape_image = QuarterCircle(size, shape_color, 180).draw()

        if shape_index == 9:
            shape_image = HalfCircle(size, shape_color, 180).draw()

        if shape_index == 10:
            shape_image = HalfCircle(size, shape_color, 90).draw()

        if shape_index == 11:
            shape_image = HalfCircle(size, shape_color, 0).draw()

        if shape_index == 12:
            shape_image = HalfCircle(size, shape_color, -90).draw()

        if shape_index == 13:
            shape_image = Cross(int(size * 1.5), shape_color, 0).draw()

        if shape_index == 14:
            shape_image = Cross(int(size * 1.5), shape_color, 45).draw()

        if shape_index == 15:
            shape_image = Triangle(int(size * 1.5), int(size * 1.5 / 2 * math.sqrt(3)), shape_color, 0).draw()

        if shape_index == 16:
            shape_image = Triangle(int(size * 1.5), int(size * 1.5 / 2 * math.sqrt(3)), shape_color, 60).draw()

        if shape_index == 17:
            shape_image = Square(size, shape_color, 45).draw()

        if shape_index == 18:
            shape_image = Square(size, shape_color, 0).draw()

        if shape_index == 19:
            shape_image = Rectangle(size, int(size * 1.5), shape_color, 0).draw()

        if shape_index == 20:
            shape_image = Rectangle(size, int(size * 1.5), shape_color, 90).draw()

        if shape_index == 21:
            shape_image = Trapezoid(size / 2, size, size / 2, shape_color, 0).draw()

        if shape_index == 22:
            shape_image = Trapezoid(size / 2, size, size / 2, shape_color, 180).draw()

        if shape_index == 23:
            shape_image = Pentagon(size / 2, shape_color, 36).draw()

        if shape_index == 24:
            shape_image = Pentagon(size / 2, shape_color, 0).draw()

        if shape_index == 25:
            shape_image = Hexagon(size / 2, shape_color, 0).draw()

        if shape_index == 26:
            shape_image = Hexagon(size / 2, shape_color, 30).draw()

        if shape_index == 27:
            shape_image = Heptagon(size / 2, shape_color, 180).draw()

        if shape_index == 28:
            shape_image = Heptagon(size / 2, shape_color, 0).draw()

        if shape_index == 29:
            shape_image = Octagon(size / 2, shape_color, 0).draw()

        if shape_index == 30:
            shape_image = Octagon(size / 2, shape_color, 22.5).draw()

        if shape_index == 31:
            shape_image = Star(int(size / 1.5), shape_color, 180).draw()

        if shape_index == 32:
            shape_image = Star(int(size / 1.5), shape_color, 0).draw()

        cropped_shape_image = BoundedImageCropper.crop_bounded_image(shape_image, shape_image.load(), shape_color)
        letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0) / proportionality), letter_color).generate_specified_letter()

        if shape_index == 15:
            return ImagePaster.paste_images_triangle_angle_up(cropped_shape_image, letter_image)

        if shape_index == 16:
            return ImagePaster.paste_images_triangle_side_up(cropped_shape_image, letter_image)

        if shape_index == 23 or shape_index == 31:
            return ImagePaster.paste_images_pentagon_angle_up(cropped_shape_image, letter_image)

        if shape_index == 24 or shape_index == 32:
            return ImagePaster.paste_images_pentagon_side_up(cropped_shape_image, letter_image)

        if shape_index == 2:
            return ImagePaster.paste_images_quarter_circle_ur(cropped_shape_image, letter_image)

        if shape_index == 4:
            return ImagePaster.paste_images_quarter_circle_dr(cropped_shape_image, letter_image)

        if shape_index == 6:
            return ImagePaster.paste_images_quarter_circle_dl(cropped_shape_image, letter_image)

        if shape_index == 8:
            return ImagePaster.paste_images_quarter_circle_ul(cropped_shape_image, letter_image)

        else:
            return ImagePaster.paste_images(cropped_shape_image, letter_image)

    #@staticmethod
    #def create_specified_single_target_with_background():
