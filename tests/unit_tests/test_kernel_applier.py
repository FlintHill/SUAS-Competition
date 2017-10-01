from SyntheticDataset.image_operations import Point
import unittest
from SyntheticDataset.image_operations import KernelApplier
from PIL import Image

class KernelApplierTestCase(unittest.TestCase):

    def setUp(self):
        #self.test_kernel1 = [[32,25,26], [30,20,26], [35,25,26]]
        #self.test_kernel1 = [[0,-1,0], [-1,5,-1], [0,-1,0]]
        self.test_kernel1 = [[0,0,0], [0,1,0], [0,0,0]]
        self.kernelSum = KernelApplier.getKernelSum(self.test_kernel1)

    def test_get_kernel_sum(self):
        self.assertEqual(1, self.kernelSum)

    def test_apply_kernal_to_pixel(self):
        img = Image.open('tests/images/target.PNG')
        image = img.load()
        P1 = KernelApplier.applyKernelToPixel(Point(35,25),img, image, self.test_kernel1, self.kernelSum)
        P2 = KernelApplier.applyKernelToPixel(Point(34,30),img, image, self.test_kernel1, self.kernelSum)
        P3 = KernelApplier.applyKernelToPixel(Point(37,34),img, image, self.test_kernel1, self.kernelSum)
        self.assertEqual((224,203,129,255), P1)
        self.assertEqual((114,183,100,255), P2)
        self.assertEqual((202,198,123,255), P3)
        #self.assertEqual((51038, 48838, 30493, 255), P)
        #self.self.assertEqual(, P)

    def test_apply_kernal_to_pixel_with_alpha(self):
        img = Image.open('tests/images/target.PNG')
        image = img.load()
        P1 = KernelApplier.applyKernelToPixel(Point(35,25),img, image, self.test_kernel1, self.kernelSum)
        P2 = KernelApplier.applyKernelToPixel(Point(34,30),img, image, self.test_kernel1, self.kernelSum)
        P3 = KernelApplier.applyKernelToPixel(Point(37,34),img, image, self.test_kernel1, self.kernelSum)
        self.assertEqual((224,203,129,255), P1)
        self.assertEqual((114,183,100,255), P2)
        self.assertEqual((202,198,123,255), P3)
        #self.assertEqual((51038, 48838, 30493, 62215), P)

    def test_get_img_applied_with_kernel(self):
        img = Image.open('tests/images/target.PNG')
        image = img.load()
        I = KernelApplier.getImgAppliedWithKernel(img, image, self.test_kernel1)
        loaded_I = I.load()

        self.assertEqual(image[34,24], loaded_I[34,24])
        self.assertEqual(image[35,24], loaded_I[35,24])
        self.assertEqual(image[36,24], loaded_I[36,24])
        self.assertEqual(image[37,24], loaded_I[37,24])


    def test_get_img_applied_with_kernel_with_alpha(self):
        img = Image.open('tests/images/target.PNG')
        image = img.load()
        I = KernelApplier.getImgAppliedWithKernelWithAlpha(img, image, self.test_kernel1)
        loaded_I = I.load()

        self.assertEqual(image[22,34], loaded_I[22,34])
        self.assertEqual(image[23,34], loaded_I[23,34])
        self.assertEqual(image[24,34], loaded_I[24,34])
        self.assertEqual(image[25,34], loaded_I[25,34])
        self.assertEqual(image[26,34], loaded_I[26,34])
