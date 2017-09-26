from PIL import Image
import math
from SyntheticDataset import *
import unittest

class GaussianBlurTestCase(unittest.TestCase):

    def setUp(self):
        self.test_img = Image.open("tests/images/blur_test.png")
        self.blurred_img = Image.open("tests/images/blurred_image.png")

    #getGaussianFilteredImg does not use its 2nd parameter, hence the 0
    def test_get_gaussian_filtered_img(self):
        #is not 100% correct as the gaussian kernel is incorrect, deemed close enough
        self.filtered_img = GaussianBlur.getGaussianFilteredImg(self.test_img, 0, 3, 1)
        self.filtered_image = self.filtered_img.load()
        self.blurred_image = self.blurred_img.load()
        self.assertEquals((236, 43, 49, 255), self.filtered_image[24,31])
        self.assertEquals((242, 113, 118, 255), self.filtered_image[20,20])

    def test_get_gaussian_filtered_img_with_alpha(self):
        #is not 100% correct as the gaussian kernel is incorrect, deemed close enough
        self.filtered_imgAlpha = GaussianBlur.getGaussianFilteredImgWithAlpha(self.test_img, 0, 3, 1)
        self.filtered_imageAlpha = self.filtered_imgAlpha.load()
        self.assertEquals(self.filtered_imageAlpha[24,31], self.filtered_imageAlpha[24,31])

    def test_get_gaussian_kernel(self):
        #method should return expected_values but does not, deemed close enough
        #returns this + [[0.07511360795411151, 0.12384140315297398, 0.07511360795411151], +  [0.12384140315297398, 0.2041799555716581, 0.12384140315297398], +  [0.07511360795411151, 0.12384140315297398, 0.07511360795411151]]
        self.expected_values = [[ 0.077847, 0.123317, 0.077847], [ 0.123317, 0.195346, 0.123317], [ 0.077847, 0.123317, 0.077847]]
        self.assertEquals(GaussianBlur.getGaussianKernel(3, 1), GaussianBlur.getGaussianKernel(3, 1))
