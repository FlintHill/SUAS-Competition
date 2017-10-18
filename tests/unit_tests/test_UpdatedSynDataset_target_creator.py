import unittest
import math
from PIL import Image
from SyntheticDataset2.ElementsCreator import *
from SyntheticDataset2.ImageOperations import *
from SyntheticDataset2.ImageCreator import *

class TargetCreatorTestCase(unittest.TestCase):

    def setUp(self):
        self.test_image0 = TargetCreator.create_specified_single_target(0, "A", 300, 2, (255, 255, 255, 255), (0, 255, 255, 255))
        self.test_image1 = TargetCreator.create_specified_single_target(1, "A", 300, 2, (255, 255, 255, 255), (0, 255, 255, 255))
        self.test_image2 = TargetCreator.create_specified_single_target(2, "B", 300, 2, (255, 255, 255, 255), (0, 255, 255, 255))
        self.test_image3 = TargetCreator.create_specified_single_target(3, "C", 300, 2, (255, 255, 255, 255), (0, 255, 255, 255))
        self.test_image4 = TargetCreator.create_specified_single_target(4, "D", 300, 2, (255, 255, 255, 255), (0, 255, 255, 255))
        self.test_image5 = TargetCreator.create_specified_single_target(5, "E", 400, 2, (0, 0, 0, 255), (255, 255, 255, 255))
        self.test_image6 = TargetCreator.create_specified_single_target(6, "F", 400, 2, (0, 0, 0, 255), (255, 255, 255, 255))
        self.test_image7 = TargetCreator.create_specified_single_target(7, "G", 400, 2, (0, 0, 0, 255), (255, 255, 255, 255))
        self.test_image8 = TargetCreator.create_specified_single_target(8, "H", 400, 2, (0, 0, 0, 255), (255, 255, 255, 255))
        self.test_image9 = TargetCreator.create_specified_single_target(9, "I", 500, 2, (255, 0, 0, 255), (0, 0, 0, 255))
        self.test_image10 = TargetCreator.create_specified_single_target(10, "J", 500, 2, (255, 0, 0, 255), (0, 0, 0, 255))
        self.test_image11 = TargetCreator.create_specified_single_target(11, "K", 500, 2, (255, 0, 0, 255), (0, 0, 0, 255))
        self.test_image12 = TargetCreator.create_specified_single_target(12, "L", 500, 2, (255, 0, 0, 255), (0, 0, 0, 255))
        self.test_image13 = TargetCreator.create_specified_single_target(13, "M", 600, 2, (0, 255, 0, 255), (255, 0, 0, 255))
        self.test_image14 = TargetCreator.create_specified_single_target(14, "N", 600, 2, (0, 255, 0, 255), (255, 0, 0, 255))
        self.test_image15 = TargetCreator.create_specified_single_target(15, "O", 600, 2, (0, 255, 0, 255), (255, 0, 0, 255))
        self.test_image16 = TargetCreator.create_specified_single_target(16, "P", 600, 2, (0, 255, 0, 255), (255, 0, 0, 255))
        self.test_image17 = TargetCreator.create_specified_single_target(17, "Q", 700, 3, (0, 0, 255, 255), (0, 255, 0, 255))
        self.test_image18 = TargetCreator.create_specified_single_target(18, "R", 700, 3, (0, 0, 255, 255), (0, 255, 0, 255))
        self.test_image19 = TargetCreator.create_specified_single_target(19, "S", 700, 3, (0, 0, 255, 255), (0, 255, 0, 255))
        self.test_image20 = TargetCreator.create_specified_single_target(20, "T", 700, 3, (0, 0, 255, 255), (0, 255, 0, 255))
        self.test_image21 = TargetCreator.create_specified_single_target(21, "U", 800, 3, (255, 255, 0, 255), (0, 0, 255, 255))
        self.test_image22 = TargetCreator.create_specified_single_target(22, "V", 800, 3, (255, 255, 0, 255), (0, 0, 255, 255))
        self.test_image23 = TargetCreator.create_specified_single_target(23, "W", 800, 3, (255, 255, 0, 255), (0, 0, 255, 255))
        self.test_image24 = TargetCreator.create_specified_single_target(24, "X", 800, 3, (255, 255, 0, 255), (0, 0, 255, 255))
        self.test_image25 = TargetCreator.create_specified_single_target(25, "Y", 900, 3, (255, 0, 255, 255), (255, 255, 0, 255))
        self.test_image26 = TargetCreator.create_specified_single_target(26, "Z", 900, 3, (255, 0, 255, 255), (255, 255, 0, 255))
        self.test_image27 = TargetCreator.create_specified_single_target(27, "A", 900, 3, (255, 0, 255, 255), (255, 255, 0, 255))
        self.test_image28 = TargetCreator.create_specified_single_target(28, "B", 900, 3, (255, 0, 255, 255), (255, 255, 0, 255))
        self.test_image29 = TargetCreator.create_specified_single_target(29, "C", 1000, 3, (0, 255, 255, 255), (255, 0, 255, 255))
        self.test_image30 = TargetCreator.create_specified_single_target(30, "D", 1000, 3, (0, 255, 255, 255), (255, 0, 255, 255))
        self.test_image31 = TargetCreator.create_specified_single_target(31, "E", 1000, 3, (0, 255, 255, 255), (255, 0, 255, 255))
        self.test_image32 = TargetCreator.create_specified_single_target(31, "F", 1000, 3, (0, 255, 255, 255), (255, 0, 255, 255))

    def test_create_specified_single_target(self):
        self.assertTrue(abs(self.test_image0.width - 300) < 3)
        self.assertTrue(abs(self.test_image0.height - 300) < 3)

        self.assertTrue(abs(self.test_image1.width - (300 * math.sqrt(2))) < 3)
        self.assertTrue(abs(self.test_image1.height - 300) < 3)

        self.assertTrue(abs(self.test_image2.width - 300) < 3)
        self.assertTrue(abs(self.test_image2.height - 300) < 3)

        self.assertTrue(abs(self.test_image3.width - 300) < 3)
        self.assertTrue(abs(self.test_image3.height - (300 * math.sqrt(2))) < 3)

        self.assertTrue(abs(self.test_image4.width - 300) < 3)
        self.assertTrue(abs(self.test_image4.height - 300) < 3)

        self.assertTrue(abs(self.test_image5.width - (400 * math.sqrt(2))) < 3)
        self.assertTrue(abs(self.test_image5.height - 400) < 3)

        self.assertTrue(abs(self.test_image6.width - 400) < 3)
        self.assertTrue(abs(self.test_image6.height - 400) < 3)

        self.assertTrue(abs(self.test_image7.width - 400) < 3)
        self.assertTrue(abs(self.test_image7.height - (400 * math.sqrt(2))) < 3)

        self.assertTrue(abs(self.test_image8.width - 400) < 3)
        self.assertTrue(abs(self.test_image8.height - 400) < 3)

        self.assertTrue(abs(self.test_image9.width - 1000) < 3)
        self.assertTrue(abs(self.test_image9.height - 500) < 3)

        self.assertTrue(abs(self.test_image10.width - 500) < 3)
        self.assertTrue(abs(self.test_image10.height - 1000) < 3)

        self.assertTrue(abs(self.test_image11.width - 1000) < 3)
        self.assertTrue(abs(self.test_image11.height - 500) < 3)

        self.assertTrue(abs(self.test_image12.width - 500) < 3)
        self.assertTrue(abs(self.test_image12.height - 1000) < 3)

        self.assertTrue(abs(self.test_image13.width - 900) < 3)
        self.assertTrue(abs(self.test_image13.height - 900) < 3)

        self.assertTrue(abs(self.test_image14.width - (600 * math.sqrt(2))) < 3)
        self.assertTrue(abs(self.test_image14.height - (600 * math.sqrt(2))) < 3)

        self.assertTrue(abs(self.test_image15.width - 900) < 3)
        self.assertTrue(abs(self.test_image15.height - (450 * math.sqrt(3))) < 3)

        self.assertTrue(abs(self.test_image16.width - 900) < 3)
        self.assertTrue(abs(self.test_image16.height - (450 * math.sqrt(3))) < 3)

        self.assertTrue(abs(self.test_image17.width - (700 * math.sqrt(2))) < 3)
        self.assertTrue(abs(self.test_image17.height - (700 * math.sqrt(2))) < 3)

        self.assertTrue(abs(self.test_image18.width - 700) < 3)
        self.assertTrue(abs(self.test_image18.height - 700) < 3)

        self.assertTrue(abs(self.test_image19.width - 700) < 3)
        self.assertTrue(abs(self.test_image19.height - 1050) < 3)

        self.assertTrue(abs(self.test_image20.width - 1050) < 3)
        self.assertTrue(abs(self.test_image20.height - 700) < 3)

        self.assertTrue(abs(self.test_image21.width - 800) < 3)
        self.assertTrue(abs(self.test_image21.height - 400) < 3)

        self.assertTrue(abs(self.test_image22.width - 800) < 3)
        self.assertTrue(abs(self.test_image22.height - 400) < 3)

        self.assertTrue(abs(self.test_image23.width - (800 * math.sin(math.radians(72)))) < 3)
        self.assertTrue(abs(self.test_image23.height - (400 + (400 * math.cos(math.radians(36))))) < 3)

        self.assertTrue(abs(self.test_image24.width - (800 * math.sin(math.radians(72)))) < 3)
        self.assertTrue(abs(self.test_image24.height - (400 + (400 * math.cos(math.radians(36))))) < 3)

        self.assertTrue(abs(self.test_image25.width - (450 * math.sqrt(3))) < 3)
        self.assertTrue(abs(self.test_image25.height - 900) < 3)

        self.assertTrue(abs(self.test_image26.width - 900) < 3)
        self.assertTrue(abs(self.test_image26.height - (450 * math.sqrt(3))) < 3)

        self.assertTrue(abs(self.test_image27.width - (900 * math.sin(math.radians(540/7)))) < 3)
        self.assertTrue(abs(self.test_image27.height - (450 + (450 * math.cos(math.radians(360/14))))) < 3)

        self.assertTrue(abs(self.test_image28.width - (900 * math.sin(math.radians(540/7)))) < 3)
        self.assertTrue(abs(self.test_image28.height - (450 + (450 * math.cos(math.radians(360/14))))) < 3)

        self.assertTrue(abs(self.test_image29.width - 1000) < 3)
        self.assertTrue(abs(self.test_image29.height - 1000) < 3)

        self.assertTrue(abs(self.test_image30.width - (1000 * math.cos(math.radians(22.5)))) < 3)
        self.assertTrue(abs(self.test_image30.height - (1000 * math.cos(math.radians(22.5)))) < 3)

        self.assertTrue(abs(self.test_image31.width - (2 * 1000 / 1.5 * math.sin(math.radians(72)))) < 3)
        self.assertTrue(abs(self.test_image31.height - ((1000 / 1.5) + (1000 / 1.5 * math.cos(math.radians(36))))) < 3)

        self.assertTrue(abs(self.test_image32.width - (2 * 1000 / 1.5 * math.sin(math.radians(72)))) < 3)
        self.assertTrue(abs(self.test_image32.height - ((1000 / 1.5) + (1000 / 1.5 * math.cos(math.radians(36))))) < 3)
