from SyntheticDataset.image_operations import Point
import unittest
from SyntheticDataset.image_operations import KernelApplier
from PIL import Image

class KernelApplierTestCase(unittest.TestCase):

    def setUp(self):
        self.test_kernel1 = [[0,0,0], [0,1,0], [0,0,0]]
        self.kernelsum = KernelApplier.getKernelSum(self.test_kernel1)

    def test_get_kernel_sum(self):
        self.assertEqual(1, self.kernelsum)

    def test_apply_kernal_to_pixel(self):
        img = Image.open('tests/images/target.PNG')
        image = img.load()
        P1 = KernelApplier.applyKernelToPixel(Point(35,25),img, image, self.test_kernel1, self.kernelsum)
        P2 = KernelApplier.applyKernelToPixel(Point(34,30),img, image, self.test_kernel1, self.kernelsum)
        P3 = KernelApplier.applyKernelToPixel(Point(37,34),img, image, self.test_kernel1, self.kernelsum)
        self.assertEqual((224,203,129,255), P1)
        self.assertEqual((114,183,100,255), P2)
        self.assertEqual((202,198,123,255), P3)

    def test_apply_kernal_to_pixel_with_alpha(self):
        img = Image.open('tests/images/target.PNG')
        image = img.load()
        P1 = KernelApplier.applyKernelToPixelWithAlpha(Point(35,25),img, image, self.test_kernel1, self.kernelsum)
        P2 = KernelApplier.applyKernelToPixelWithAlpha(Point(34,30),img, image, self.test_kernel1, self.kernelsum)
        P3 = KernelApplier.applyKernelToPixelWithAlpha(Point(37,34),img, image, self.test_kernel1, self.kernelsum)
        self.assertEqual((224,203,129,255), P1)
        self.assertEqual((114,183,100,255), P2)
        self.assertEqual((202,198,123,255), P3)

    def test_get_img_applied_with_kernel(self):
        img = Image.open('tests/images/target.PNG')
        image = img.load()
        test_image = KernelApplier.getImgAppliedWithKernel(img, image, self.test_kernel1)
        loaded_Image = test_image.load()

        self.assertEqual(image[34,24], loaded_Image[34,24])
        self.assertEqual(image[35,24], loaded_Image[35,24])
        self.assertEqual(image[36,24], loaded_Image[36,24])
        self.assertEqual(image[37,24], loaded_Image[37,24])

    def test_get_img_applied_with_kernel_with_alpha(self):
        img = Image.open('tests/images/target.PNG')
        image = img.load()
        test_image = KernelApplier.getImgAppliedWithKernelWithAlpha(img, image, self.test_kernel1)
        loaded_Image = test_image.load()

        self.assertEqual(image[22,34], loaded_Image[22,34])
        self.assertEqual(image[23,34], loaded_Image[23,34])
        self.assertEqual(image[24,34], loaded_Image[24,34])
        self.assertEqual(image[25,34], loaded_Image[25,34])
        self.assertEqual(image[26,34], loaded_Image[26,34])
