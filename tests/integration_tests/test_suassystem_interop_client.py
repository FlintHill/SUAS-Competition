import unittest
import interop
from SUASSystem import InteropClientConverter
from SUASSystem import Location

class SDATestCase(unittest.TestCase):

    def setUp(self):
        self.msl_alt = 6
        self.connection_url = "http://10.10.130.2:8000"
        self.username = "flint"
        self.password = "8182105855"

        self.interop_client = InteropClientConverter(self.msl_alt, self.connection_url, self.username, self.password)

    def test_submit_target(self):
        compiled_target_info = {
            "location" : interop.GpsPosition(latitude=38, longitude=76),
            "orientation" : interop.Orientation.s,
            "shape" : interop.Shape.circle,
            "background_color" : interop.Color.white,
            "alphanumeric" : "ABC",
            "alphanumeric_color" : interop.Color.black,
        }
        target_image_relative_path = "tests/images/target.png"

        target_id = self.interop_client.post_standard_target(compiled_target_info, target_image_relative_path)
        self.assertTrue(target_id != None)

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
