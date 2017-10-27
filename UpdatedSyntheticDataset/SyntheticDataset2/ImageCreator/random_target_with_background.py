from PIL import Image
import random
from .settings import Settings
from .random_target import RandomTarget
from SyntheticDataset2.ElementsCreator.background import BackgroundGenerator
from SyntheticDataset2.logger import Logger

class RandomTargetWithBackground(object):

    def __init__(self):
        self.size_range = Settings.TARGET_SIZE_RANGE_IN_PIXELS
        self.proportionality_range = Settings.PROPORTIONALITY_RANGE
        self.pixelization_level = Settings.PIXELIZATION_LEVEL
        self.noise_level = Settings.NOISE_LEVEL

        self.random_target = RandomTarget(self.size_range, self.proportionality_range, self.pixelization_level, self.noise_level)

        self.new_target_dimension = random.randint(Settings.TARGET_SIZE_RANGE_IN_PIXELS[0], Settings.TARGET_SIZE_RANGE_IN_PIXELS[1])
        self.target_image = self.random_target.create_random_target()

        if self.target_image.width >= self.target_image.height:
            self.new_target_width = self.new_target_dimension
            self.new_target_height = self.new_target_dimension * self.target_image.height / self.target_image.width
        else:
            self.new_target_height = self.new_target_dimension
            self.new_target_width = self.new_target_dimension * self.target_image.width / self.target_image.height

    def create_random_target_with_background(self):
        resized_target_image = self.target_image.resize((self.new_target_width, self.new_target_height))
        self.background = BackgroundGenerator(Settings.BACKGROUND_DIRECTORY).generate_specific_background(resized_target_image.width + 20, resized_target_image.height + 20)
        self.background.paste(resized_target_image, (10, 10), resized_target_image)

        Logger.log("Target's Dimension in pixels: " + str(self.new_target_dimension + 20)
                   + "\nNew Target's Dimension in inches: " + str(float(self.new_target_dimension + 20) / Settings.PPSI))

        return self.background

    def record_random_target_with_background(self):
        self.random_target.record_random_target()
        text = open(Settings.TEXT_SAVING_PATH + "/tester.txt", "a")
        text.write("\nCenter of Target: (" + str(10 + (self.new_target_width / 2)) + ", " + str(10 + (self.new_target_height / 2)) + ")")

        self.background.save(Settings.IMAGE_SAVING_PATH + "/tester.PNG")
