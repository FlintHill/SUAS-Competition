import unittest, math
from SUASSystem import Location, GCSSettings, inverse_haversine
from SUASSystem.utils import get_image_timestamp, get_target_gps_location

class ImageOperationsTestCase(unittest.TestCase):

    def test_get_image_timestamp(self):
        self.test_filename = "image1234567889910.jpg"
        self.assertEqual(get_image_timestamp(self.test_filename), 1234567889910)

        self.test_filename = "image0.jpg"
        self.assertEqual(get_image_timestamp(self.test_filename), 0)

    def test_get_target_gps_location(self):
        self.test_drone_gps_location = Location(0,0,100)
        self.test_image_midpoint = (100,100)
        self.test_target_midpoint = (50,50)

        self.difference_vector = ((self.test_target_midpoint[0] - self.test_image_midpoint[0]) / math.sqrt(GCSSettings.IMAGE_PROC_PPSI) / 12, (self.test_target_midpoint[1] - self.test_image_midpoint[1]) / math.sqrt(GCSSettings.IMAGE_PROC_PPSI) / 12, 0)
        self.assertEqual(round(inverse_haversine(self.test_drone_gps_location, self.difference_vector).get_lat()), round(get_target_gps_location(self.test_image_midpoint, self.test_target_midpoint, self.test_drone_gps_location).get_lat()))

        self.test_drone_gps_location = Location(1000,1000,5)
        self.test_image_midpoint = (40,75)
        self.test_target_midpoint = (1000,510)

        self.difference_vector = ((self.test_target_midpoint[0] - self.test_image_midpoint[0]) / math.sqrt(GCSSettings.IMAGE_PROC_PPSI) / 12, (self.test_target_midpoint[1] - self.test_image_midpoint[1]) / math.sqrt(GCSSettings.IMAGE_PROC_PPSI) / 12, 0)
        self.assertEqual(round(inverse_haversine(self.test_drone_gps_location, self.difference_vector).get_lat()), round(get_target_gps_location(self.test_image_midpoint, self.test_target_midpoint, self.test_drone_gps_location).get_lat()))
