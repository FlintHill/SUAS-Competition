import unittest

from ObjAvoidSimplified import *

class MapInitializationTestCase(unittest.TestCase):

    def setUp(self):
        self.mass_holder = MassHolder([])
        self.drone_mass = DroneMass(10, [])

        self.obj_map = Map(self.mass_holder, self.drone_mass)

    def test_append_mass(self):
        """
        Test appending masses to a map
        """
        testing_mass = Mass(np.zeros(2), 100)
        self.obj_map.append_mass(testing_mass)

        map_mass_holder = self.obj_map.get_mass_holder()
        self.assertEqual(len(map_mass_holder), 1)
        self.assertEqual(map_mass_holder[0].get_mass(), testing_mass.get_mass())
        self.assertEqual(testing_mass.get_point().all(), map_mass_holder[0].get_point().all())

    def test_drone_mass(self):
        """
        Test drone mass initialization
        """
        map_drone_mass = self.obj_map.get_drone_mass()
        self.assertEqual(map_drone_mass.get_mass(), self.drone_mass.get_mass())

    def test_drone_waypoints(self):
        """
        Test waypoint addition for drone masses
        """
        waypoint = np.array([10, 10])
        self.obj_map.add_waypoint(waypoint)

        self.assertEqual(len(self.obj_map.get_drone_mass().get_waypoint_holder()), 1)
