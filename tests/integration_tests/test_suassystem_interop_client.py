import unittest
import interop
from SUASSystem import InteropClientConverter
from SUASSystem import Location

class SDATestCase(unittest.TestCase):

    def setUp(self):
        self.interop_client = InteropClientConverter()

    def test_submit_target(self):
        compiled_target_info = {
            "latitude" : 38,
            "longitude" : -77,
            "orientation" : "s",
            "shape" : "circle",
            "background_color" : "white",
            "alphanumeric" : "ABC",
            "alphanumeric_color" : "black",
        }
        target_image_relative_path = "tests/images/target.PNG"

        target_id = self.interop_client.post_standard_target(compiled_target_info, target_image_relative_path)

    def test_submit_position(self):
        """
        Test POST of position data
        """
        self.interop_client.post_telemetry(Location(38, 76, 100), 350.0)

    def test_get_obstacles(self):
        """
        Test GET of obstacles
        """
        self.interop_client.get_obstacles()

    def test_get_active_mission(self):
        """
        Test GET of active mission
        """
        self.interop_client.get_active_mission()
