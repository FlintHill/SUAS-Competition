from PIL import Image
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
    """
    self.shapelist =
    [circle,
    quarter_circle_u, quarter_circle_ur, quarter_circle_r, quarter_circle_dr, quarter_circle_d, quarter_circle_dl, quarter_circle_l, quarter_circle_ul,
    half_circle_u, half_circle_r, half_circle_d, half_circle4_l,
    cross_cv, cross2_cc,
    triangle_a, triangle_s,
    square_a, square_s,
    rectangle_s, rectangle_l,
    trapezoid_s, trapezoid_l,
    pentagon_a, pentagon_s,
    hexagon_a, hexagon_s,
    heptagon_a, heptagon_s,
    octagon_a, octagon_s,
    star_cv, star_cc]
    """

    @staticmethod
    def create_specified_single_target(shape_index, letter, size, proportionality, shape_color, letter_color):
        font_type = "UpdatedSyntheticDataset/data/fonts/Blockletter.otf"
        if shape_index == 0:
            shape_image = Circle(size * proportionality / 2, shape_color).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 1:
            shape_image = QuarterCircle(size * proportionality, shape_color, 135).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 2:
            shape_image = QuarterCircle(size * proportionality, shape_color, 90).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 3:
            shape_image = QuarterCircle(size * proportionality, shape_color, 45).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 4:
            shape_image = QuarterCircle(size * proportionality, shape_color, 0).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 5:
            shape_image = QuarterCircle(size * proportionality, shape_color, -45).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 6:
            shape_image = QuarterCircle(size * proportionality, shape_color, -90).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 7:
            shape_image = QuarterCircle(size * proportionality, shape_color, -135).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 8:
            shape_image = QuarterCircle(size * proportionality, shape_color, 180).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 9:
            shape_image = HalfCircle(size * proportionality, shape_color, 180).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 10:
            shape_image = HalfCircle(size * proportionality, shape_color, 90).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 11:
            shape_image = HalfCircle(size * proportionality, shape_color, 0).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 12:
            shape_image = HalfCircle(size * proportionality, shape_color, -90).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 13:
            shape_image = Cross(int(size * proportionality * 1.5), shape_color, 0).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 14:
            shape_image = Cross(int(size * proportionality * 1.5), shape_color, 45).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)
        """
        if shape_index == 15:

        if shape_index == 16:
        """

        if shape_index == 17:
            shape_image = Square(size * proportionality, shape_color, 45).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 18:
            shape_image = Square(size * proportionality, shape_color, 0).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 19:
            shape_image = Rectangle(size * proportionality, size * proportionality * 2, shape_color, 0).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 20:
            shape_image = Rectangle(size * proportionality, size * proportionality * 2, shape_color, 90).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 21:
            shape_image = Trapezoid(size * proportionality, size * proportionality * 2, size * proportionality, shape_color, 0).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 22:
            shape_image = Trapezoid(size * proportionality, size * proportionality * 2, size * proportionality, shape_color, 180).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 23:
            shape_image = Pentagon(size * proportionality / 2, shape_color, 32).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 24:
            shape_image = Pentagon(size * proportionality / 2, shape_color, 0).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 25:
            shape_image = Hexagon(size * proportionality / 2, shape_color, 30).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 26:
            shape_image = Hexagon(size * proportionality / 2, shape_color, 0).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 27:
            shape_image = Heptagon(size * proportionality / 2, shape_color, 180/7).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 28:
            shape_image = Heptagon(size * proportionality / 2, shape_color, 0).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 29:
            shape_image = Octagon(size * proportionality / 2, shape_color, 22.5).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 30:
            shape_image = Octagon(size * proportionality / 2, shape_color, 0).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 31:
            shape_image = Star(int(size * proportionality / 1.5), shape_color, 180).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

        if shape_index == 32:
            shape_image = Star(int(size * proportionality / 1.5), shape_color, 0).draw()
            letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0)), letter_color).generate_specified_letter()
            return ImagePaster.paste_images(shape_image, letter_image)

    #@staticmethod
    #def create_target_with_background():
