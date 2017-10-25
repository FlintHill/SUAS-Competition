from PIL import Image
import math
from .settings import Settings
from SyntheticDataset2.ElementsCreator import *
from SyntheticDataset2.ImageOperations.shape_orientator import ShapeOrientator
from SyntheticDataset2.ImageOperations.bounded_image_cropper import BoundedImageCropper
from SyntheticDataset2.ImageOperations.image_paster import ImagePaster
from SyntheticDataset2.ImageOperations.shape_rotator import ShapeRotator
from SyntheticDataset2.ImageOperations.image_resizer import ImageResizer

class SpecifiedTargetCreator(object):

    @staticmethod
    def create_specified_target(shape_type, shape_orientation, letter, size, proportionality_level, shape_color, letter_color, rotation, pixelization_level, noise_level):
        """
        :param shape_type: the type of the shape to be created.
        :param shape_orientation: the intended orientation of the shape, modified with ShapeOrientator.
        :param letter: the letter to be created.
        :param size: a parameter of the sizes of the shapes. Different shapes have different ways to use "size"
                     (for circles, radius is a function of "size"; for squares, side length is a function of "size", etc.)
        :param proportionality_level: a parameter of the proportionality between the shapes and the letters.
                                "proportionality_level" is a value, not a specific proportionality between the
                                dimensions of the shapes and letters as different shapes fit differently with
                                the letters. 1.5 should be the max value of "proportionality_level". Increasing
                                "proportionality_level" increases the size of the shape while the size of the letter
                                stays constant.
        :param shape_color: the color of the shape.
        :param letter_color: the color of the letter.
        :param rotation: the intended rotation of the combined image of shape and letter.
        :param pixelization_level: the level of pixelization, see the first method of ImageResizer
        :param noise_level: the intended level of noise. (See gaussian_noise_generator for detail.)

        :type shape_type: string (see ShapeTypes)
        :type shape_orientation: string (see ShapeOrientator)
        :type letter: string
        :type size: int (representing pixel)
        :type proportionality_level: float (ideally between 1.5 and 2.5)
        :type shape_color: (R, G, B, A) (:type R, G, B, and A: int from 0 to 255)
        :type letter_color: (R, G, B, A) (:type R, G, B, and A: int from 0 to 255)
        :type rotation: float
        :type pixelization_level: float (preferably below 20.0)
        :type noise_level: float (0.0 to 100.0)
        """
        font_type = Settings.FONT_TYPE

        if shape_type == ShapeTypes.CIRCLE:
            shape_image = Circle(size / 2, shape_color).draw()

        elif shape_type == ShapeTypes.QUARTERCIRCLE:
            shape_image = QuarterCircle(int(size * 1.5), shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        elif shape_type == ShapeTypes.HALFCIRCLE:
            shape_image = HalfCircle(size, shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        elif shape_type == ShapeTypes.CROSS:
            shape_image = Cross(int(size * 2), shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        elif shape_type == ShapeTypes.TRIANGLE:
            shape_image = Triangle(int(size * 1.5 / math.sqrt(3) * 2), int(size * 1.5), shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        elif shape_type == ShapeTypes.SQUARE:
            shape_image = Square(size, shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        elif shape_type == ShapeTypes.RECTANGLE:
            shape_image = Rectangle(size, int(size * 1.5), shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        elif shape_type == ShapeTypes.TRAPEZOID:
            shape_image = Trapezoid(size, int(size * 1.5), size, shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        elif shape_type == ShapeTypes.PENTAGON:
            shape_image = Pentagon(int(size / 1.7), shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        elif shape_type == ShapeTypes.HEXAGON:
            shape_image = Hexagon(int(size / 1.8), shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        elif shape_type == ShapeTypes.HEPTAGON:
            shape_image = Heptagon(int(size / 1.8), shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        elif shape_type == ShapeTypes.OCTAGON:
            shape_image = Octagon(int(size / 1.8), shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        else:
            shape_image = Star(int(size / 1.1), shape_color, ShapeOrientator.orientate_shape(shape_type, shape_orientation)).draw()

        cropped_shape_image = BoundedImageCropper.crop_bounded_image(shape_image, shape_image.load(), shape_color)
        letter_image = SpecifiedLetterGenerator(letter, font_type, int(size*(10000.0 / 6832.0) / proportionality_level), letter_color).generate_specified_letter()

        if shape_type == ShapeTypes.TRIANGLE:
            if shape_orientation == ShapeOrientations.NORTH:
                shape_with_letter = ImagePaster.paste_images_triangle_angle_north(cropped_shape_image, letter_image)

            elif shape_orientation == ShapeOrientations.SOUTH:
                shape_with_letter = ImagePaster.paste_images_triangle_angle_south(cropped_shape_image, letter_image)

        elif shape_type == ShapeTypes.PENTAGON or shape_type == ShapeTypes.STAR:
            if shape_orientation == ShapeOrientations.NORTH:
                shape_with_letter = ImagePaster.paste_images_pentagon_angle_north(cropped_shape_image, letter_image)

            elif shape_orientation == ShapeOrientations.SOUTH:
                shape_with_letter = ImagePaster.paste_images_pentagon_angle_south(cropped_shape_image, letter_image)

        elif shape_type == ShapeTypes.QUARTERCIRCLE:
            if shape_orientation == ShapeOrientations.NORTHEAST:
                shape_with_letter = ImagePaster.paste_images_quarter_circle_northeast(cropped_shape_image, letter_image)

            elif shape_orientation == ShapeOrientations.SOUTHEAST:
                shape_with_letter = ImagePaster.paste_images_quarter_circle_southeast(cropped_shape_image, letter_image)

            elif shape_orientation == ShapeOrientations.SOUTHWEST:
                shape_with_letter = ImagePaster.paste_images_quarter_circle_southwest(cropped_shape_image, letter_image)

            elif shape_orientation == ShapeOrientations.NORTHWEST:
                shape_with_letter = ImagePaster.paste_images_quarter_circle_northwest(cropped_shape_image, letter_image)

            else:
                shape_with_letter = ImagePaster.paste_images(cropped_shape_image, letter_image)

        else:
            shape_with_letter = ImagePaster.paste_images(cropped_shape_image, letter_image)

        if rotation != 0 or rotation != 180 or rotation != 360:
            rotated_image = ShapeRotator.rotate_shape(shape_with_letter, rotation, shape_color)

        else:
            rotated_image = shape_with_letter

        resized_image = ImageResizer.resize_image_conserved(rotated_image, pixelization_level)
        return NoisedImageGenerator.generate_noised_image_by_level(resized_image, noise_level)
