from PIL import Image
import random
from .settings import Settings
from .specified_target_creator import SpecifiedTargetCreator
from .random_target_creator import RandomTargetCreator
from SyntheticDataset2.ElementsCreator.background import BackgroundGenerator

class TargetWithBackgroundCreator(object):

    @staticmethod
    def create_specified_target_with_random_background(shape_type, shape_orientation, letter, shape_color, letter_color, rotation):
        """
        :param shape_type: the type of the shape to be created.
        :param shape_orientation: the intended orientation of the shape, modified with ShapeOrientator.
        :param letter: the letter to be created.
        :param shape_color: the color of the shape.
        :param letter_color: the color of the letter.
        :param rotation: the intended rotation of the combined image of shape and letter.

        :type shape_type: string (see ShapeTypes)
        :type shape_orientation: string (see ShapeOrientator)
        :type letter: string
        :type shape_color: (R, G, B, A) (:type R, G, B, and A: int from 0 to 255)
        :type letter_color: (R, G, B, A) (:type R, G, B, and A: int from 0 to 255)
        :type rotation: float
        """
        size = Settings.SINGLE_TARGET_SIZE_IN_PIXELS
        proportionality = Settings.SINGLE_TARGET_PROPORTIONALITY
        pixelization_level = Settings.PIXELIZATION_LEVEL
        noise_level = Settings.NOISE_LEVEL

        target_image = SpecifiedTargetCreator.create_specified_target(shape_type, shape_orientation, letter, size, proportionality, shape_color, letter_color, rotation, pixelization_level, noise_level)

        new_target_dimension = Settings.SINGLE_TARGET_SIZE_IN_PIXELS

        if target_image.width >= target_image.height:
            new_target_width = new_target_dimension
            new_target_height = new_target_dimension * target_image.height / target_image.width
        else:
            new_target_height = new_target_dimension
            new_target_width = new_target_dimension * target_image.width / target_image.height

        resized_target_image = target_image.resize((new_target_width, new_target_height))

        background = BackgroundGenerator(Settings.BACKGROUND_DIRECTORY).generate_specific_background(resized_target_image.width + 20, resized_target_image.height + 20)
        background.paste(resized_target_image, (10, 10), resized_target_image)
        return background

    @staticmethod
    def create_random_target_with_random_background():
        size_range = [Settings.TARGET_GENERATION_SIZE_IN_PIXELS, Settings.TARGET_GENERATION_SIZE_IN_PIXELS]
        proportionality_range = Settings.PROPORTIONALITY_RANGE
        pixelization_level = Settings.PIXELIZATION_LEVEL
        noise_level = Settings.NOISE_LEVEL

        target_image = RandomTargetCreator.create_random_target(size_range, proportionality_range, pixelization_level, noise_level)

        new_target_dimension = random.randint(Settings.TARGET_SIZE_RANGE_IN_PIXELS[0], Settings.TARGET_SIZE_RANGE_IN_PIXELS[1])

        if target_image.width >= target_image.height:
            new_target_width = new_target_dimension
            new_target_height = new_target_dimension * target_image.height / target_image.width
        else:
            new_target_height = new_target_dimension
            new_target_width = new_target_dimension * target_image.width / target_image.height

        resized_target_image = target_image.resize((new_target_width, new_target_height))

        background = BackgroundGenerator(Settings.BACKGROUND_DIRECTORY).generate_specific_background(resized_target_image.width + 20, resized_target_image.height + 20)
        background.paste(resized_target_image, (10, 10), resized_target_image)
        print "New Target's Dimension in pixels: " + str(new_target_dimension + 20)
        return background
