import random
import numpy
from SyntheticDataset.image_operations import *
from SyntheticDataset.color import *
import string
import math
import timeit
import os

class SyntheticImage(object):
    """
    Generates a list of targets and places them on a single image
    """

    def __init__(self, num_targets, background_image, data_path):
        self.targets = []
        self.num_targets = num_targets
        self.synthetic_image = background_image.copy()
        self.background_image = background_image
        self.data_path = data_path

        self.variance_theta = math.pi/32.0
        self.min_width = 75
        self.min_height = 75
        self.max_width = 200
        self.max_height = 200
        self.blur_kernel_size = 3
        self.blur_std_dev = 2
        self.grass_blur_std_dev = 2

        self.generate_targets()

    def get_synthetic_image(self):
        """
        Return the synthetic image
        """
        return self.synthetic_image

    def get_targets(self):
        """
        Return the targets generated
        """
        return self.targets

    def asDict(self):
        """
        Return the dictionary representation of the synthetic image
        """
        dictionary_representation = [target.asDict() for target in self.targets]

        return dictionary_representation

    def generate_targets(self):
        """
        Generate all of the targets and place them on the image
        """
        for index in range(self.num_targets):
            random_target = self.get_randomly_generated_target()

            self.targets.append(random_target)
            self.paste_target_on_image(random_target)

    def paste_target_on_image(self, target):
        """
        Paste a target on the image
        """
        target.fill(self.synthetic_image, self.synthetic_image.load())

    def get_randomly_generated_target(self):
        shape = self.get_random_shape_type()
        bounds = self.get_random_location()
        color = ColorList.getRandomColor()
        letter = self.get_random_letter()

        fieldObject = Target(shape, bounds, self.get_random_angle(), color, letter, self.data_path)

        return fieldObject

    def get_random_angle(self):
        rand_base_theta = random.randint(0,8)*(math.pi/4.0)
        variance_theta = random.random()* self.variance_theta - (self.variance_theta / 2)
        return rand_base_theta + variance_theta

    def get_random_letter(self):
        letters = dict(enumerate(string.ascii_uppercase, 0))
        randIndex = random.randint(0, len(letters) - 1)
        return letters[randIndex]

    def get_random_location(self):
        randWidth = random.randint(self.min_width, self.max_width)
        randHeight = random.randint(self.min_height, self.max_height)
        randX = random.randint(0, self.background_image.size[0]-randWidth-1)
        randY = random.randint(0, self.background_image.size[1]-randHeight-1)

        random_location_rectangle = Rectangle(randX, randY, randWidth, randHeight)
        for target in self.targets:
            bounding_rectangle = target.get_bounding_rectangle()

            if random_location_rectangle.intersects(bounding_rectangle):
                random_location_rectangle = self.get_random_location()

        return random_location_rectangle

    def get_random_shape_type(self):
        return Target.possibleShapes[int(random.random() * len(Target.possibleShapes))]
