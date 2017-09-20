import random
import numpy
from SyntheticDataset.image_operations import *
from SyntheticDataset.color import *
import string
import math
import timeit
import os
import unittest
from PIL import Image

class TestSyntheticImage(unittest.TestCase):

    def test_get_synthetic_image(self):
        im = image.open('ball.jpg')
        image = SyntheticImage(2,im,3)
        realImage = image.get_synthetic_image()
