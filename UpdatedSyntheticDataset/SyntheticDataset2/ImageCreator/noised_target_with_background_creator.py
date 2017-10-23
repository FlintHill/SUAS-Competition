from PIL import Image
import random
from SyntheticDataset2.ElementsCreator.background import BackgroundGenerator
from SyntheticDataset2.ElementsCreator.noised_image_generator import NoisedImageGenerator
from .specified_target_creator import SpecifiedTargetCreator
from .random_target_creator import RandomTargetCreator

class NoisedTargetWithBackgroundCreator(object):

    @staticmethod
    def create_specified_noised_target_with_random_background(shape_type, shape_orientation, letter, size, proportionality, shape_color, letter_color, rotation, path_to_backgrounds, noise_level):
        """
        :param shape_type: the type of the shape to be created.
        :param shape_orientation: the intended orientation of the shape, modified with ShapeOrientator.
        :param letter: the letter to be created.
        :param size: a parameter of the sizes of the shapes. See specified_target_creator for detail.
        :param proportionality_level: a intended level of proportionality between the shapes and the letters.
                                      (See specified_target_creator for detail.)
        :param shape_color: the color of the shape.
        :param letter_color: the color of the letter.
        :param rotation: the intended rotation of the combined image of shape and letter.
        :param path_to_backgrounds: the directory of backgrounds
        :param noise_level: the intended level of noise. (See gaussian_noise_generator for detail.)

        :type shape_type: string (see ShapeTypes)
        :type shape_orientation: string (see ShapeOrientator)
        :type letter: string
        :type size: int (representing pixel)
        :type proportionality_level: float (ideally between 1.5 and 2.5)
        :type shape_color: (R, G, B, A) (:type R, G, B, and A: int from 0 to 255)
        :type letter_color: (R, G, B, A) (:type R, G, B, and A: int from 0 to 255)
        :type rotation: float
        :type path_to_backgrounds: directory
        :type noise_level: float (0.0 to 100.0)
        """
        target_image = SpecifiedTargetCreator.create_specified_target(shape_type, shape_orientation, letter, size, proportionality, shape_color, letter_color, rotation)
        noised_target_image = NoisedImageGenerator.generate_noised_image_by_level(target_image, noise_level)
        background = BackgroundGenerator(noised_target_image.width, noised_target_image.height, path_to_backgrounds).generate_background()

        random_x_min = random.randint(10, background.width - noised_target_image.width - 20)
        random_y_min = random.randint(10, background.height - noised_target_image.height - 20)

        cropped_background = background.crop((random_x_min, random_y_min,
                                              random_x_min + noised_target_image.width + 20,
                                              random_y_min + noised_target_image.height + 20))

        cropped_background.paste(noised_target_image, (10, 10), noised_target_image)
        return cropped_background

    @staticmethod
    def create_specified_noised_target_with_specified_background(shape_type, shape_orientation, letter, size, proportionality, shape_color, letter_color, rotation, path_to_background, noise_level):
        """
        :param path_to_background: the specific path to the image of background
        :type path_to_background: an image file
        """
        target_image = SpecifiedTargetCreator.create_specified_target(shape_type, shape_orientation, letter, size, proportionality, shape_color, letter_color, rotation)
        noised_target_image = NoisedImageGenerator.generate_noised_image_by_level(target_image, noise_level)
        background = Image.open(path_to_background)

        random_x_min = random.randint(10, background.width - noised_target_image.width - 20)
        random_y_min = random.randint(10, background.height - noised_target_image.height - 20)

        cropped_background = background.crop((random_x_min, random_y_min,
                                              random_x_min + noised_target_image.width + 20,
                                              random_y_min + noised_target_image.height + 20))

        cropped_background.paste(noised_target_image, (10, 10), noised_target_image)
        return cropped_background

    @staticmethod
    def create_random_noised_target_with_random_background(size_range, proportionality_range, path_to_backgrounds, noise_level):
        """
        :param size_range: the range of sizes that are to be selected randomly
        :param proportionality_range: the range of proportionality levels that are to be selected randomly
        :type size_range: [min_size, max_size] //:type min_size and max_size: int
        :type proportionality_range: [min_proportionality, max_proportionality] //:type min_proportionality and max_proportionality: double
        """
        target_image = RandomTargetCreator.create_random_target(size_range, proportionality_range)
        noised_target_image = NoisedImageGenerator.generate_noised_image_by_level(target_image, noise_level)
        background = BackgroundGenerator(noised_target_image.width, noised_target_image.height, path_to_backgrounds).generate_background()

        random_x_min = random.randint(10, background.width - noised_target_image.width - 20)
        random_y_min = random.randint(10, background.height - noised_target_image.height - 20)

        cropped_background = background.crop((random_x_min, random_y_min,
                                              random_x_min + noised_target_image.width + 20,
                                              random_y_min + noised_target_image.height + 20))

        cropped_background.paste(noised_target_image, (10, 10), noised_target_image)
        return cropped_background

    @staticmethod
    def create_random_noised_target_with_specified_background(size_range, proportionality_range, path_to_background, noise_level):
        target_image = RandomTargetCreator.create_random_target(size_range, proportionality_range)
        noised_target_image = NoisedImageGenerator.generate_noised_image_by_level(target_image, noise_level)
        background = Image.open(path_to_background)

        random_x_min = random.randint(10, background.width - noised_target_image.width - 20)
        random_y_min = random.randint(10, background.height - noised_target_image.height - 20)

        cropped_background = background.crop((random_x_min, random_y_min,
                                              random_x_min + noised_target_image.width + 20,
                                              random_y_min + noised_target_image.height + 20))

        cropped_background.paste(noised_target_image, (10, 10), noised_target_image)
        return cropped_background
