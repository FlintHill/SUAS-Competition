from PIL import Image
import math
from .settings import Settings
from SyntheticDataset2.ElementsCreator import *
from SyntheticDataset2.ImageOperations.shape_orientator import ShapeOrientator
from SyntheticDataset2.ImageOperations.bounded_image_cropper import BoundedImageCropper
from SyntheticDataset2.ImageOperations.image_paster import ImagePaster
from SyntheticDataset2.ImageOperations.shape_rotator import ShapeRotator
from SyntheticDataset2.ImageOperations.image_resizer import ImageResizer

class SpecifiedTarget(object):

    def __init__(self, shape_type, shape_orientation, letter, size, proportionality_level, shape_color, letter_color, rotation, pixelization_level, noise_level):
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
        self.shape_type = shape_type
        self.shape_orientation = shape_orientation
        self.letter = letter
        self.size = size
        self.proportionality_level = proportionality_level
        self.shape_color = shape_color
        self.letter_color = letter_color
        self.rotation = rotation
        self.pixelization_level = pixelization_level
        self.noise_level = noise_level

    def create_specified_target(self):
        if self.shape_type == ShapeTypes.CIRCLE:
            shape_image = Circle(self.size / 2, self.shape_color).draw()

        elif self.shape_type == ShapeTypes.QUARTERCIRCLE:
            shape_image = QuarterCircle(int(self.size * 1.5), self.shape_color, ShapeOrientator.orientate_shape(self.shape_type, self.shape_orientation)).draw()

        elif self.shape_type == ShapeTypes.HALFCIRCLE:
            shape_image = HalfCircle(self.size, self.shape_color, ShapeOrientator.orientate_shape(self.shape_type, self.shape_orientation)).draw()

        elif self.shape_type == ShapeTypes.CROSS:
            shape_image = Cross(self.size * 2, self.shape_color, ShapeOrientator.orientate_shape(self.shape_type, self.shape_orientation)).draw()

        elif self.shape_type == ShapeTypes.TRIANGLE:
            shape_image = Triangle(int(self.size * 1.5 / math.sqrt(3) * 2), int(self.size * 1.5), self.shape_color, ShapeOrientator.orientate_shape(self.shape_type, self.shape_orientation)).draw()

        elif self.shape_type == ShapeTypes.SQUARE:
            shape_image = Square(self.size, self.shape_color, ShapeOrientator.orientate_shape(self.shape_type, self.shape_orientation)).draw()

        elif self.shape_type == ShapeTypes.RECTANGLE:
            shape_image = Rectangle(self.size, int(self.size * 1.5), self.shape_color, ShapeOrientator.orientate_shape(self.shape_type, self.shape_orientation)).draw()

        elif self.shape_type == ShapeTypes.TRAPEZOID:
            shape_image = Trapezoid(self.size, int(self.size * 1.5), self.size, self.shape_color, ShapeOrientator.orientate_shape(self.shape_type, self.shape_orientation)).draw()

        elif self.shape_type == ShapeTypes.PENTAGON:
            shape_image = Pentagon(int(self.size / 1.7), self.shape_color, ShapeOrientator.orientate_shape(self.shape_type, self.shape_orientation)).draw()

        elif self.shape_type == ShapeTypes.HEXAGON:
            shape_image = Hexagon(int(self.size / 1.8), self.shape_color, ShapeOrientator.orientate_shape(self.shape_type, self.shape_orientation)).draw()

        elif self.shape_type == ShapeTypes.HEPTAGON:
            shape_image = Heptagon(int(self.size / 1.8), self.shape_color, ShapeOrientator.orientate_shape(self.shape_type, self.shape_orientation)).draw()

        elif self.shape_type == ShapeTypes.OCTAGON:
            shape_image = Octagon(int(self.size / 1.8), self.shape_color, ShapeOrientator.orientate_shape(self.shape_type, self.shape_orientation)).draw()

        else:
            shape_image = Star(int(self.size / 1.1), self.shape_color, ShapeOrientator.orientate_shape(self.shape_type, self.shape_orientation)).draw()

        cropped_shape_image = BoundedImageCropper.crop_bounded_image(shape_image, shape_image.load(), self.shape_color)
        letter_image = SpecifiedLetterGenerator(self.letter, Settings.FONT_TYPE, int(self.size*(10000.0 / 6832.0) / self.proportionality_level), self.letter_color).generate_specified_letter()

        if self.shape_type == ShapeTypes.TRIANGLE:
            if self.shape_orientation == ShapeOrientations.NORTH:
                shape_with_letter = ImagePaster.paste_images_triangle_angle_north(cropped_shape_image, letter_image)

            elif self.shape_orientation == ShapeOrientations.SOUTH:
                shape_with_letter = ImagePaster.paste_images_triangle_angle_south(cropped_shape_image, letter_image)

        elif self.shape_type == ShapeTypes.PENTAGON or self.shape_type == ShapeTypes.STAR:
            if self.shape_orientation == ShapeOrientations.NORTH:
                shape_with_letter = ImagePaster.paste_images_pentagon_angle_north(cropped_shape_image, letter_image)

            elif self.shape_orientation == ShapeOrientations.SOUTH:
                shape_with_letter = ImagePaster.paste_images_pentagon_angle_south(cropped_shape_image, letter_image)

        elif self.shape_type == ShapeTypes.QUARTERCIRCLE:
            if self.shape_orientation == ShapeOrientations.NORTHEAST:
                shape_with_letter = ImagePaster.paste_images_quarter_circle_northeast(cropped_shape_image, letter_image)

            elif self.shape_orientation == ShapeOrientations.SOUTHEAST:
                shape_with_letter = ImagePaster.paste_images_quarter_circle_southeast(cropped_shape_image, letter_image)

            elif self.shape_orientation == ShapeOrientations.SOUTHWEST:
                shape_with_letter = ImagePaster.paste_images_quarter_circle_southwest(cropped_shape_image, letter_image)

            elif self.shape_orientation == ShapeOrientations.NORTHWEST:
                shape_with_letter = ImagePaster.paste_images_quarter_circle_northwest(cropped_shape_image, letter_image)

            else:
                shape_with_letter = ImagePaster.paste_images(cropped_shape_image, letter_image)

        else:
            shape_with_letter = ImagePaster.paste_images(cropped_shape_image, letter_image)

        if self.rotation != 0 or self.rotation != 180 or self.rotation != 360:
            rotated_image = ShapeRotator.rotate_shape(shape_with_letter, self.rotation, self.shape_color)

        else:
            rotated_image = shape_with_letter

        resized_image = ImageResizer.resize_image_conserved(rotated_image, self.pixelization_level)
        return NoisedImageGenerator.generate_noised_image_by_level(resized_image, self.noise_level)

    def record_specified_target(self, file_name):
        text = open(Settings.TEXT_SAVING_PATH + "/" + file_name + ".txt", "w+")
        text.write("Shape Type: " + str(self.shape_type)
                   + "\nAlphanumeric Value: " + str(self.letter)
                   + "\nShape Color: " + str(self.shape_color)
                   + "\nAlphanumeric Color: " + str(self.letter_color)
                   + "\nOrientation: " + str(self.rotation))
