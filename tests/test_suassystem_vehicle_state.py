import unittest
from SUASSystem import *

class SUASSystemVehicleState(unittest.TestCase):

    def setUp(self):
        self.lat = 45.0
        self.lon = 78.23
        self.alt = 1.23
        self.direction = 33.33
        self.groundspeed = 532.1
        self.velocity = numpy.array([10,20,30])
        self.obstacle_in_path = True
        self.current_waypoint_number = 4

    def test_get_direction(self):
        test_vehicle_state = VehicleState(self.lat, self.lon, self.alt, self.direction, self.groundspeed, self.velocity, self.obstacle_in_path, self.current_waypoint_number)

        self.assertEqual(test_vehicle_state.get_direction(), self.direction)

    def test_get_groudspeed(self):
        test_vehicle_state = VehicleState(self.lat, self.lon, self.alt, self.direction, self.groundspeed, self.velocity, self.obstacle_in_path, self.current_waypoint_number)

        self.assertEqual(test_vehicle_state.get_groundspeed(), self.groundspeed)

    def test_get_velocity(self):
        test_vehicle_state = VehicleState(self.lat, self.lon, self.alt, self.direction, self.groundspeed, self.velocity, self.obstacle_in_path, self.current_waypoint_number)

        calculated_velocity = (sum(self.velocity**2))**0.5
        calculated_velocity *= GCSSettings.KNOTS_PER_METERS_PER_SECOND

        self.assertEqual(test_vehicle_state.get_velocity(), calculated_velocity)

    def test_get_obstacle_in_path(self):
        test_vehicle_state = VehicleState(self.lat, self.lon, self.alt, self.direction, self.groundspeed, self.velocity, self.obstacle_in_path, self.current_waypoint_number)

        self.assertEqual(test_vehicle_state.get_obstacle_in_path(), self.obstacle_in_path)

    def test_get_location(self):
        test_vehicle_state = VehicleState(self.lat, self.lon, self.alt, self.direction, self.groundspeed, self.velocity, self.obstacle_in_path, self.current_waypoint_number)

        self.assertEqual(test_vehicle_state.lat, self.lat)
        self.assertEqual(test_vehicle_state.lon, self.lon)
        self.assertEqual(test_vehicle_state.alt, self.alt)

    def test_get_current_waypoint_number(self):
        test_vehicle_state = VehicleState(self.lat, self.lon, self.alt, self.direction, self.groundspeed, self.velocity, self.obstacle_in_path, self.current_waypoint_number)

        self.assertEqual(test_vehicle_state.current_waypoint_number, self.current_waypoint_number)
