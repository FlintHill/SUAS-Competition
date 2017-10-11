import unittest
from PIL import Image
from SyntheticDataset2.ElementsCreator import *
from SyntheticDataset2.ImageOperations import *

class NoisedImageGeneratorTestCase(unittest.TestCase):

    def setUp(self):
        self.font_type = "UpdatedSyntheticDataset/data/fonts/Blockletter.otf"

        self.test_image1 = SpecifiedLetterGenerator("I", self.font_type, 200, (255, 255, 0, 255)).generate_specified_letter()
        self.test_image2 = SpecifiedLetterGenerator("N", self.font_type, 400, (255, 0, 255, 255)).generate_specified_letter()
        self.test_image3 = SpecifiedLetterGenerator("F", self.font_type, 600, (0, 255, 255, 255)).generate_specified_letter()
        self.test_image4 = SpecifiedLetterGenerator("Z", self.font_type, 800, (233, 233, 233, 255)).generate_specified_letter()
        self.test_image5 = SpecifiedLetterGenerator("Y", self.font_type, 1000, (123, 123, 123, 255)).generate_specified_letter()
        self.test_image6 = SpecifiedLetterGenerator("I", self.font_type, 1200, (255, 255, 0, 255)).generate_specified_letter()
        self.test_image7 = SpecifiedLetterGenerator("N", self.font_type, 1400, (255, 0, 255, 255)).generate_specified_letter()
        self.test_image8 = SpecifiedLetterGenerator("F", self.font_type, 1600, (0, 255, 255, 255)).generate_specified_letter()
        self.test_image9 = SpecifiedLetterGenerator("Z", self.font_type, 1800, (233, 233, 233, 255)).generate_specified_letter()
        self.test_image10 = SpecifiedLetterGenerator("Y", self.font_type, 2000, (123, 123, 123, 255)).generate_specified_letter()

        self.test_image_a1 = NoisedImageGenerator.generate_noised_image_by_level(self.test_image1.copy(), 2)
        self.test_image_a2 = NoisedImageGenerator.generate_noised_image_by_level(self.test_image2.copy(), 4)
        self.test_image_a3 = NoisedImageGenerator.generate_noised_image_by_level(self.test_image3.copy(), 6)
        self.test_image_a4 = NoisedImageGenerator.generate_noised_image_by_level(self.test_image4.copy(), 8)
        self.test_image_a5 = NoisedImageGenerator.generate_noised_image_by_level(self.test_image5.copy(), 10)
        self.test_image_a6 = NoisedImageGenerator.generate_noised_image_by_level(self.test_image6.copy(), 12)
        self.test_image_a7 = NoisedImageGenerator.generate_noised_image_by_level(self.test_image7.copy(), 14)
        self.test_image_a8 = NoisedImageGenerator.generate_noised_image_by_level(self.test_image8.copy(), 16)
        self.test_image_a9 = NoisedImageGenerator.generate_noised_image_by_level(self.test_image9.copy(), 18)
        self.test_image_a10 = NoisedImageGenerator.generate_noised_image_by_level(self.test_image10.copy(), 20)

        self.test_image_b1 = NoisedImageGenerator.generate_noised_image_by_radius(self.test_image1.copy(), 2)
        self.test_image_b2 = NoisedImageGenerator.generate_noised_image_by_radius(self.test_image2.copy(), 4)
        self.test_image_b3 = NoisedImageGenerator.generate_noised_image_by_radius(self.test_image3.copy(), 6)
        self.test_image_b4 = NoisedImageGenerator.generate_noised_image_by_radius(self.test_image4.copy(), 8)
        self.test_image_b5 = NoisedImageGenerator.generate_noised_image_by_radius(self.test_image5.copy(), 10)
        self.test_image_b6 = NoisedImageGenerator.generate_noised_image_by_radius(self.test_image6.copy(), 12)
        self.test_image_b7 = NoisedImageGenerator.generate_noised_image_by_radius(self.test_image7.copy(), 14)
        self.test_image_b8 = NoisedImageGenerator.generate_noised_image_by_radius(self.test_image8.copy(), 16)
        self.test_image_b9 = NoisedImageGenerator.generate_noised_image_by_radius(self.test_image9.copy(), 18)
        self.test_image_b10 = NoisedImageGenerator.generate_noised_image_by_radius(self.test_image10.copy(), 20)

    def test_generate_noised_image_by_level(self):
        self.assertTrue(abs(self.test_image_a1.width - self.test_image1.width) < int(6 * self.test_image1.width * 2/200+1))
        self.assertTrue(abs(self.test_image_a1.height - self.test_image1.height) < int(6 * self.test_image1.width * 2/200+1))

        self.assertTrue(abs(self.test_image_a2.width - self.test_image2.width) < int(6 * self.test_image2.width * 4/200+1))
        self.assertTrue(abs(self.test_image_a2.height - self.test_image2.height) < int(6 * self.test_image2.width * 4/200+1))

        self.assertTrue(abs(self.test_image_a3.width - self.test_image3.width) < int(6 * self.test_image3.width * 6/200+1))
        self.assertTrue(abs(self.test_image_a3.height - self.test_image3.height) < int(6 * self.test_image3.width * 6/200+1))

        self.assertTrue(abs(self.test_image_a4.width - self.test_image4.width) < int(6 * self.test_image4.width * 8/200+1))
        self.assertTrue(abs(self.test_image_a4.height - self.test_image4.height) < int(6 * self.test_image4.width * 8/200+1))

        self.assertTrue(abs(self.test_image_a5.width - self.test_image5.width) < int(6 * self.test_image5.width * 10/200+1))
        self.assertTrue(abs(self.test_image_a5.height - self.test_image5.height) < int(6 * self.test_image5.width * 10/200+1))

        self.assertTrue(abs(self.test_image_a6.width - self.test_image6.width) < int(6 * self.test_image6.width * 12/200+1))
        self.assertTrue(abs(self.test_image_a6.height - self.test_image6.height) < int(6 * self.test_image6.width * 12/200+1))

        self.assertTrue(abs(self.test_image_a7.width - self.test_image7.width) < int(6 * self.test_image7.width * 14/200+1))
        self.assertTrue(abs(self.test_image_a7.height - self.test_image7.height) < int(6 * self.test_image7.width * 14/200+1))

        self.assertTrue(abs(self.test_image_a8.width - self.test_image8.width) < int(6 * self.test_image8.width * 16/200+1))
        self.assertTrue(abs(self.test_image_a8.height - self.test_image8.height) < int(6 * self.test_image8.width * 16/200+1))

        self.assertTrue(abs(self.test_image_a9.width - self.test_image9.width) < int(6 * self.test_image9.width * 18/200+1))
        self.assertTrue(abs(self.test_image_a9.height - self.test_image9.height) < int(6 * self.test_image9.width * 18/200+1))

        self.assertTrue(abs(self.test_image_a10.width - self.test_image10.width) < int(6 * self.test_image10.width * 20/200+1))
        self.assertTrue(abs(self.test_image_a10.height - self.test_image10.height) < int(6 * self.test_image10.width * 20/200+1))

    def test_generate_noised_image_by_radius(self):
        self.assertTrue(abs(self.test_image_b1.width - self.test_image1.width) < 6 * 2)
        self.assertTrue(abs(self.test_image_b1.height - self.test_image1.height) < 6 * 2)

        self.assertTrue(abs(self.test_image_b2.width - self.test_image2.width) < 6 * 4)
        self.assertTrue(abs(self.test_image_b2.height - self.test_image2.height) < 6 * 4)

        self.assertTrue(abs(self.test_image_b3.width - self.test_image3.width) < 6 * 6)
        self.assertTrue(abs(self.test_image_b3.height - self.test_image3.height) < 6 * 6)

        self.assertTrue(abs(self.test_image_b4.width - self.test_image4.width) < 6 * 8)
        self.assertTrue(abs(self.test_image_b4.height - self.test_image4.height) < 6 * 8)

        self.assertTrue(abs(self.test_image_b5.width - self.test_image5.width) < 6 * 10)
        self.assertTrue(abs(self.test_image_b5.height - self.test_image5.height) < 6 * 10)

        self.assertTrue(abs(self.test_image_b6.width - self.test_image6.width) < 6 * 12)
        self.assertTrue(abs(self.test_image_b6.height - self.test_image6.height) < 6 * 12)

        self.assertTrue(abs(self.test_image_b7.width - self.test_image7.width) < 6 * 14)
        self.assertTrue(abs(self.test_image_b7.height - self.test_image7.height) < 6 * 14)

        self.assertTrue(abs(self.test_image_b8.width - self.test_image8.width) < 6 * 16)
        self.assertTrue(abs(self.test_image_b8.height - self.test_image8.height) < 6 * 16)

        self.assertTrue(abs(self.test_image_b9.width - self.test_image9.width) < 6 * 18)
        self.assertTrue(abs(self.test_image_b9.height - self.test_image9.height) < 6 * 18)

        self.assertTrue(abs(self.test_image_b10.width - self.test_image10.width) < 6 * 20)
        self.assertTrue(abs(self.test_image_b10.height - self.test_image10.height) < 6 * 20)
