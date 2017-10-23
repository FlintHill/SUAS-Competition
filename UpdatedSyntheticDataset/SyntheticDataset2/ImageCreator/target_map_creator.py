from PIL import Image
import random
from SyntheticDataset2.ElementsCreator.background import BackgroundGenerator
from .random_target_creator import RandomTargetCreator

class TargetMapCreator(object):

    @staticmethod
    def create_random_target_map(number_of_targets, size_range, proportionality_range, path_to_backgrounds):
        """
        Create a map with a specified number of random targets.

        :param number_of_targets: the number of targets to be created.
        :param size_range: the range of sizes that are to be selected randomly
        :param proportionality_range: the range of proportionality levels that are to be selected randomly
        :param path_to_backgrounds: the directory of images of background
        :type number_of_targets: int
        :type size_range: [min_size, max_size] //:type min_size and max_size: int
        :type proportionality_range: [min_proportionality, max_proportionality] //:type min_proportionality and max_proportionality: double
        :type path_to_backgrounds: directory
        """
        i = 0
        background = BackgroundGenerator(max(size_range) * number_of_targets * 2, max(size_range) * number_of_targets * 2, path_to_backgrounds).generate_background()
        while i < number_of_targets:
            target_image = RandomTargetCreator.create_random_target(size_range, proportionality_range).rotate(random.randint(0, 181))
            background.paste(target_image, (random.randint(0, background.width - target_image.width), random.randint(0, background.height - target_image.height)), target_image)
            i = i + 1
        return background
