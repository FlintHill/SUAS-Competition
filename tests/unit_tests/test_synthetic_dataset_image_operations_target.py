import unittest
#from SyntheticDataset.image_operations import *
import random
import os
from PIL import Image
import numpy

class TestSytheticDatasetImageOperationsTarget(unittest.TestCase):

    def setUp(self):
        #class constants
        self.grassColor = target.grassColor
        self.lowerLetterRadiusBound = target.lowerLetterRadiusBound
        self.upperLetterRadiusBound = target.upperLetterRadiusBound
        self.possibleShapes = target.possibleShapes

        self.shapeTypeIn = 0
        self.boundingBoxIn = 0
        self.rotationIn = 0
        self.colorIn = 0
        self.letterIn = 0
        self.data_path = 0

    #def test_set_object_letter(self):
