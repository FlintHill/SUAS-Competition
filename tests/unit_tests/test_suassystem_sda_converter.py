import unittest
from SUASSystem import *
from SDA import *
import numpy
import interop

class SDAConverterTestCase(unittest.TestCase):

    def setUp(self):

        #Initialize

        self.setup_client_converter()

    def setup_client_converter(self):
        self.initial_coordinates = Location(38.8703041, -77.3214035, 0)
        self.boundary_points = [
            {
                "boundary_pts" : [
                    {"latitude" : 38.8697558739, "longitude" : -77.3221076688, "order" : 0},
                    {"latitude" : 38.8708523261, "longitude" : -77.3221076743, "order" : 0},
                    {"latitude" : 38.8697558739, "longitude" : -77.3206993312, "order" : 0},
                    {"latitude" : 38.8708523261, "longitude" : -77.3206993257, "order" : 0}
                ]
            }
        ]

        self.sda_converter = SDAConverter(self.initial_coordinates, self.boundary_points)

    def test_convert_fly_zones(self):
        result_from_the_program=self.sda_converter.convert_fly_zones(numpy.array([self.boundary_points]))
        test_location1=Location(self.boundary_points[0]["boundary_pts"][0]["latitude"],self.boundary_points[0]["boundary_pts"][0]["longitude"],0)
        expected_result=(convert_to_point(self.initial_coordinates,test_location1)[:2])
        self.assertEqual(expected_result[0], result_from_the_program[0][0][0])
        self.assertEqual(expected_result[1], result_from_the_program[0][0][1])

    def test_convert_fly_zone(self):
        result_fly_zone=self.sda_converter.convert_fly_zone(self.boundary_points)
        test_location1=Location(self.boundary_points[0]["boundary_pts"][0]["latitude"],self.boundary_points[0]["boundary_pts"][0]["longitude"],0)
        expected_fly_zone=(convert_to_point(self.initial_coordinates,test_location1)[:2])
        self.assertEqual(expected_fly_zone[0], result_fly_zone[0][0])
        self.assertEqual(expected_fly_zone[1], result_fly_zone[0][1])

    def test_does_guided_path_exist(self):
        self.sda_converter.set_guided_path(numpy.array([numpy.array([1,2,3]),numpy.array([2,2,3])]))
        self.assertTrue(self.sda_converter.does_guided_path_exist())
       
    def test_has_path_changed(self):
        path1=numpy.array([numpy.array([1,2,3]), numpy.array([2,2,3])])
        path2=numpy.array([numpy.array([1,2,3]), numpy.array([2,2,3]),numpy.array([3,2,3])])
        path3=numpy.array([numpy.array([1,2,3]), numpy.array([2,2,3]),numpy.array([4,2,4])])
        self.assertTrue(self.sda_converter.has_path_changed(path1,path2))
        self.assertEqual(False,self.sda_converter.has_path_changed(path2,path3))

    def test_has_uav_completed_guided_path(self):
        self.sda_converter.set_path_index(3)
        self.assertTrue(self.sda_converter.has_uav_completed_guided_path())

    def test_get_uav_avoid_coordinates(self):
        self.sda_converter.set_guided_path([numpy.array([45,45,50]),numpy.array([90,90,50])])
        actual_location = Location(38.870550801732293,-77.321086622253759,15.2399995123)
        test_location = self.sda_converter.get_uav_avoid_coordinates()
        self.assertTrue(abs(actual_location.get_lat() - test_location.get_lat()) < 0.0001)
        self.assertTrue(abs(actual_location.get_lon() - test_location.get_lon()) < 0.0001)
        self.assertTrue(abs(actual_location.get_alt() - test_location.get_alt()) < 0.0001)        

    def test_get_distance_to_current_guided_waypoint(self):
        self.sda_converter.set_guided_path(numpy.array([numpy.array([45,45,50]),numpy.array([90,90,50])]))
        self.assertEqual(136.74794331177344,self.sda_converter.get_distance_to_current_guided_waypoint())

    def test_has_uav_reached_guided_waypoint(self):
        self.sda_converter.set_guided_path(numpy.array([numpy.array([45,45,50]),numpy.array([90,90,50])]))
        self.assertEqual(False,self.sda_converter.has_uav_reached_guided_waypoint())
        returned_array=self.sda_converter.convert_fly_zones(numpy.array([self.boundary_points]))
        test_location1=Location(self.boundary_points[0]["boundary_pts"][0]["latitude"],self.boundary_points[0]["boundary_pts"][0]["longitude"],0)
        expected_result=(convert_to_point(self.initial_coordinates,test_location1)[:2])
        self.assertEqual(expected_result[0], returned_array[0][0][0])
        self.assertEqual(expected_result[1], returned_array[0][0][1])

    def test_convert_fly_zone(self):
        result_fly_zone=self.sda_converter.convert_fly_zone(self.boundary_points)
        test_location1=Location(self.boundary_points[0]["boundary_pts"][0]["latitude"],self.boundary_points[0]["boundary_pts"][0]["longitude"],0)
        expected_fly_zone=(convert_to_point(self.initial_coordinates,test_location1)[:2])
        self.assertEqual(expected_fly_zone[0], result_fly_zone[0][0])
        self.assertEqual(expected_fly_zone[1], result_fly_zone[0][1])

    def test_does_guided_path_exist(self):
        self.sda_converter.set_guided_path(numpy.array([numpy.array([1,2,3]),numpy.array([2,2,3])]))
        self.assertTrue(self.sda_converter.does_guided_path_exist())
       
    def test_has_path_changed(self):
        path1=numpy.array([numpy.array([1,2,3]), numpy.array([2,2,3])])
        path2=numpy.array([numpy.array([1,2,3]), numpy.array([2,2,3]),numpy.array([30,2,3])])
        path3=numpy.array([numpy.array([1,2,3]), numpy.array([2,2,3]),numpy.array([4,2,4])])
        self.assertTrue(self.sda_converter.has_path_changed(path1,path2))
        self.assertTrue(self.sda_converter.has_path_changed(path2,path3))

    def test_has_uav_completed_guided_path(self):
        self.sda_converter.set_path_index(3)
        self.assertTrue(self.sda_converter.has_uav_completed_guided_path())

    def test_get_uav_avoid_coordinates(self):
        self.sda_converter.obstacle_map.set_drone_position(numpy.array([0,0,0]))
        self.sda_converter.set_guided_path([numpy.array([45,45,50]),numpy.array([90,90,50])])
        actual_location = Location(38.870550801732293,-77.321086622253759,15.2399995123)
        test_location = self.sda_converter.get_uav_avoid_coordinates()
        self.assertTrue(abs(actual_location.get_lat() - test_location.get_lat()) < 0.0001)
        self.assertTrue(abs(actual_location.get_lon() - test_location.get_lon()) < 0.0001)
        self.assertTrue(abs(actual_location.get_alt() - test_location.get_alt()) < 0.0001)        

    def test_get_distance_to_current_guided_waypoint(self):
        self.sda_converter.obstacle_map.set_drone_position(numpy.array([0,0,0]))
        self.sda_converter.set_guided_path(numpy.array([numpy.array([45,45,50]),numpy.array([90,90,50])]))
        self.assertEqual(136.74794331177344,self.sda_converter.get_distance_to_current_guided_waypoint())

    def test_has_uav_reached_guided_waypoint(self):
        self.sda_converter.set_guided_path(numpy.array([numpy.array([45,45,50]),numpy.array([90,90,50])]))
        self.assertEqual(False,self.sda_converter.has_uav_reached_guided_waypoint())
        
    def test_set_waypoints(self):

        #Test the set_waypoints() method

        test_waypoint = Location(38.8742103, -77.3217697, 91.44000244140625)
        self.sda_converter.set_waypoint(test_waypoint)
        obstacle_map = self.sda_converter.obstacle_map
        waypoint_holder = obstacle_map.drone.get_waypoint_holder()
        new_gps_point = inverse_haversine(self.sda_converter.initial_coordinates,
            [waypoint_holder[0][0], waypoint_holder[0][1], 91.44000244140625])

        self.assertTrue(abs(new_gps_point.get_lat() - test_waypoint.get_lat()) < 0.004)
        self.assertTrue(abs(new_gps_point.get_lon() - test_waypoint.get_lon()) < 0.004)

    def test_add_obstacle(self):
        new_obstacle = interop.StationaryObstacle(38.8703041, -77.3214035, 0, 60.950000762939453)
        self.sda_converter.add_obstacle(Location(38.8703041, -77.3214035, 60.950000762939453), new_obstacle)
        obstacle_map = self.sda_converter.obstacle_map

        self.assertEqual(obstacle_map.obstacles.size, 1)

    def test_reset_obstacles(self):

        #Test the reset_obstacles() method

        new_obstacle = interop.StationaryObstacle(38.8703041, -77.3214035, 0, 60.950000762939453)
        self.sda_converter.add_obstacle(Location(38.8703041, -77.3214035, 60.950000762939453), new_obstacle)
        obstacle_map = self.sda_converter.obstacle_map

        self.assertEqual(obstacle_map.obstacles.size, 1)

        self.sda_converter.reset_obstacles()
        obstacle_map = self.sda_converter.obstacle_map

        self.assertEqual(obstacle_map.obstacles.size, 0)

    def test_set_uav_position(self):
        new_location = Location (40, -80, 95)
        self.sda_converter.set_uav_position(new_location)

        converted_uav_location = convert_to_point(self.initial_coordinates, new_location)

        self.assertTrue(numpy.array_equal(self.sda_converter.obstacle_map.drone.point, converted_uav_location))