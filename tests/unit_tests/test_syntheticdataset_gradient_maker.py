import unittest
from PIL import Image
from random import random
from random import sample
from random import gauss
from SyntheticDataset.image_operations import GradientMaker

class GradientMakerTestCase(unittest.TestCase):

    def setUp(self):
        self.imgDim = (4,5)
        self.stdDev = 0.267
        self.test_gradient_maker = GradientMaker.GrayGradientMaker(self.imgDim, self.stdDev)
        self.test_gradients = self.test_gradient_maker.getGradients()

    def test_fill_gradients(self):
        self.assertEqual(len(self.test_gradients), self.imgDim[0])
        self.assertEqual(len(self.test_gradients[0]), self.imgDim[1])

    def test_get_random_gradients(self):
        test_gauss = self.test_gradients[0][0]
        self.assertTrue(test_gauss < 10 and test_gauss > -10)

    def test_apply_gradients(self):
        img_orig = Image.new("RGBA", self.imgDim, "#f441af")
        image_orig = img_orig.load()

        img = Image.new("RGBA", self.imgDim, "#f441af")
        image = img.load()

        self.test_gradient_maker.applyGradients(img, image)
        self.assertNotEqual(img, img_orig)
        self.assertNotEqual(image, image_orig)
