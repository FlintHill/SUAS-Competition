from SyntheticDataset.image_operations import Point
import unittest
from SyntheticDataset.image_operations import KernelApplier
from PIL import Image

class KernelApplierTestCase(unittest.TestCase):
    def test_get_kernel_sum(self):
        kernel1 = [{32,25,26}, {30,20,26}, {35,25,26}]
        kernelSum = KernelApplier.getKernelSum(kernel1)
        self.assertEqual(30, kernel1)

    def test_apply_kernal_to_pixel(self):
        self.img = Image.open("target.jpg")
        self.image = img.load()
