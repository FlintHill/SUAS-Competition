import math
import random
from SyntheticDataset import CompassAngler
import unittest

class TestCompassAngler(unittest.TestCase):
    def test_get_compass_angles_sorted_by_proximity_to_angle(self):
        print CompassAngler.getCompassAnglesSortedByProximityToAngle(10)
