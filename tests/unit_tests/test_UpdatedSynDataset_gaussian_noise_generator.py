import unittest
from SyntheticDataset2.ElementsCreator import *
from SyntheticDataset2.ImageOperations import *
from PIL import Image

class GaussianNoiseGeneratorTestCase(unittest.TestCase):

    def setUp(self):
        self.font_type = "UpdatedSyntheticDataset/data/fonts/Blockletter.otf"

        self.test_image1 = SpecifiedLetterGenerator("X", self.font_type, 500, (0, 255, 255, 255)).generate_specified_letter()
        self.test_image2 = SpecifiedLetterGenerator("Y", self.font_type, 700, (255, 0, 255, 255)).generate_specified_letter()
        self.test_image3 = SpecifiedLetterGenerator("Z", self.font_type, 900, (255, 255, 0, 255)).generate_specified_letter()

    def test_generate_gaussian_noise_by_level(self):
        self.test_image4 = GaussianNoiseGenerator.generate_gaussian_noise_by_level(self.test_image1, 5, self.test_image1.width)
        self.test_image5 = GaussianNoiseGenerator.generate_gaussian_noise_by_level(self.test_image2, 10, self.test_image2.width)
        self.test_image6 = GaussianNoiseGenerator.generate_gaussian_noise_by_level(self.test_image3, 15, self.test_image3.width)

        self.assertFalse(self.test_image4.load()[1, 1] == (0, 255, 255, 255))
        self.assertFalse(self.test_image5.load()[1, 1] == (255, 0, 255, 255))
        self.assertTrue(self.test_image6.load()[1, 1] == (255, 255, 0, 255))

        self.assertTrue(self.test_image4.load()[self.test_image4.width/2, self.test_image4.height/2] == (0, 255, 255, 255))
        self.assertTrue(self.test_image5.load()[self.test_image5.width/2, self.test_image5.height/2] == (255, 0, 255, 255))
        self.assertFalse(self.test_image6.load()[self.test_image6.width/2, self.test_image6.height/2] == (255, 255, 0, 255))

        self.assertFalse(self.test_image4.load()[self.test_image4.width-1, self.test_image4.height-1] == (0, 255, 255, 255))
        self.assertFalse(self.test_image5.load()[self.test_image5.width-1, self.test_image5.height-1] == (255, 0, 255, 255))
        self.assertTrue(self.test_image6.load()[self.test_image6.width-1, self.test_image6.height-1] == (255, 255, 0, 255))

    def test_generate_gaussian_noise_by_radius(self):
        self.test_image7 = GaussianNoiseGenerator.generate_gaussian_noise_by_radius(self.test_image1, 5)
        self.test_image8 = GaussianNoiseGenerator.generate_gaussian_noise_by_radius(self.test_image2, 10)
        self.test_image9 = GaussianNoiseGenerator.generate_gaussian_noise_by_radius(self.test_image3, 15)

        self.test_image7.show()
        self.test_image8.show()
        self.test_image9.show()

        self.assertFalse(self.test_image7.load()[1, 1] == (0, 255, 255, 255))
        self.assertFalse(self.test_image8.load()[1, 1] == (255, 0, 255, 255))
        self.assertTrue(self.test_image9.load()[1, 1] == (255, 255, 0, 255))

        self.assertTrue(self.test_image7.load()[self.test_image7.width/2, self.test_image7.height/2] == (0, 255, 255, 255))
        self.assertTrue(self.test_image8.load()[self.test_image8.width/2, self.test_image8.height/2] == (255, 0, 255, 255))
        self.assertTrue(self.test_image9.load()[self.test_image9.width/2, self.test_image9.height/2] == (255, 255, 0, 255))

        self.assertFalse(self.test_image7.load()[self.test_image7.width-1, self.test_image7.height-1] == (0, 255, 255, 255))
        self.assertFalse(self.test_image8.load()[self.test_image8.width-1, self.test_image8.height-1] == (255, 0, 255, 255))
        self.assertTrue(self.test_image9.load()[self.test_image9.width-1, self.test_image9.height-1] == (255, 255, 0, 255))
