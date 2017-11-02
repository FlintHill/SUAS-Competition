import unittest
from SUASSystem import *
from SDA import *
import numpy
import interop

class SDAConverterTestCase(unittest.TestCase):

    def setUp(self):
        self.setup_client_converter()

    def setup_client_converter(self):
        self.initial_coordinates = Location(38.8703041, -77.3214035, 0)
        self.boundary_points = [
            {
                "boundary_pts" : [
                    {"latitude" : 38.8697558739, "longitude" : -77.3221076688, "order" : 0},
                    {"latitude" : 38.8708523261, "longitude" : -77.3221076743, "order" : 1},
                    {"latitude" : 38.8697558739, "longitude" : -77.3206993312, "order" : 2},
                    {"latitude" : 38.8708523261, "longitude" : -77.3206993257, "order" : 3}
                ]
            }
        ]

        self.sda_converter = SDAConverter(self.initial_coordinates, self.boundary_points)

    def test_convert_fly_zones(self):
        converted_fly_zones = self.sda_converter.convert_fly_zones(self.boundary_points)
        for num_of_fly_zone in range(len(converted_fly_zones)):
            for index_in_fly_zone in range(len(converted_fly_zones[num_of_fly_zone])):
                location = Location(self.boundary_points[num_of_fly_zone]["boundary_pts"][index_in_fly_zone]["latitude"], self.boundary_points[num_of_fly_zone]["boundary_pts"][index_in_fly_zone]["longitude"], 0)
                expected_converted_boundary_point = haversine(self.initial_coordinates, location, units="US")

                self.assertEqual(converted_fly_zones[num_of_fly_zone][index_in_fly_zone][0], expected_converted_boundary_point[0])
                self.assertEqual(converted_fly_zones[num_of_fly_zone][index_in_fly_zone][1], expected_converted_boundary_point[1])
    
    def test_avoid_obstacles(self):
        self.sda_converter.obstacle_map.set_drone_position(numpy.array([0,0,0]))
        self.sda_converter.reset_obstacles()
        self.sda_converter.obstacle_map.add_obstacle(StationaryObstacle(numpy.array([40,0,0]),5,100))
        test_waypoint = Location(38.8703041, -77.3210866228, 0)
        self.sda_converter.set_waypoint(test_waypoint)
        self.sda_converter.avoid_obstacles()
        boolean, possible_paths = self.sda_converter.obstacle_map.is_obstacle_in_path()
        expected_guided_path = self.sda_converter.obstacle_map.get_min_path(possible_paths)

        self.assertEqual(self.sda_converter.current_path[0][0], expected_guided_path[0][0])
        self.assertEqual(self.sda_converter.current_path[0][1], expected_guided_path[0][1])
        self.assertTrue(boolean)

    def test_get_uav_avoid_coordinates(self):
        self.sda_converter.obstacle_map.set_drone_position(numpy.array([0,0,0]))
        self.sda_converter.reset_obstacles()
        self.sda_converter.obstacle_map.add_obstacle(StationaryObstacle(numpy.array([40,0,0]),5,100))
        test_waypoint = Location(38.8703041, -77.3210866228, 0)
        self.sda_converter.set_waypoint(test_waypoint)
        self.sda_converter.avoid_obstacles()
        avoid_coordinates = self.sda_converter.get_uav_avoid_coordinates()
        converted_avoid_coordiantes = haversine(self.initial_coordinates, avoid_coordinates, units="US")
        
        self.assertEqual(int(converted_avoid_coordiantes[0]), self.sda_converter.current_path[0][0])
        self.assertEqual(int(converted_avoid_coordiantes[1]), self.sda_converter.current_path[0][1])

        avoid_coordinates.alt = avoid_coordinates.get_alt() * 3.28084
        self.sda_converter.set_uav_position(avoid_coordinates)
        avoid_coordinates2 = self.sda_converter.get_uav_avoid_coordinates()
        converted_avoid_coordiantes2 = haversine(self.initial_coordinates, avoid_coordinates2, units="US")

        self.assertEqual(int(converted_avoid_coordiantes2[0]), self.sda_converter.current_path[1][0])
        self.assertEqual(int(converted_avoid_coordiantes2[1]), self.sda_converter.current_path[1][1])        

    def test_has_uav_reached_guided_waypoint(self):
        """
        test case #1
        didn't reach the point
        """
        self.sda_converter.obstacle_map.set_drone_position(numpy.array([0,0,0]))
        self.sda_converter.reset_obstacles()
        self.sda_converter.obstacle_map.add_obstacle(StationaryObstacle(numpy.array([40,0,0]),5,100))
        test_waypoint = Location(38.8703041, -77.3210866228, 0)
        self.sda_converter.set_waypoint(test_waypoint)
        self.sda_converter.avoid_obstacles()
        
        self.assertEqual(False, self.sda_converter.has_uav_reached_guided_waypoint())
        """
        test case #2
        reached the point
        """
        self.sda_converter.obstacle_map.set_drone_position(numpy.array([0,0,0]))
        self.sda_converter.reset_obstacles()
        self.sda_converter.obstacle_map.add_obstacle(StationaryObstacle(numpy.array([40,0,0]),5,100))
        test_waypoint = Location(38.8703041, -77.3210866228, 0)
        self.sda_converter.set_waypoint(test_waypoint)
        self.sda_converter.avoid_obstacles()
        self.sda_converter.obstacle_map.set_drone_position(numpy.array([40, 35, 130]))
        
        self.assertTrue(self.sda_converter.has_uav_reached_guided_waypoint())

    def test_does_guided_path_exist(self):
        self.sda_converter.obstacle_map.set_drone_position(numpy.array([0,0,0]))
        self.sda_converter.reset_obstacles()
        self.sda_converter.obstacle_map.add_obstacle(StationaryObstacle(numpy.array([40,0,0]),5,100))
        test_waypoint = Location(38.8703041, -77.3210866228, 0)
        self.sda_converter.set_waypoint(test_waypoint)
        self.sda_converter.avoid_obstacles()

        self.assertTrue(self.sda_converter.does_guided_path_exist())

    def test_get_distance_to_current_guided_waypoint(self):
        self.sda_converter.obstacle_map.set_drone_position(numpy.array([0,0,0]))
        self.sda_converter.reset_obstacles()
        self.sda_converter.obstacle_map.add_obstacle(StationaryObstacle(numpy.array([40,0,0]),5,100))
        test_waypoint = Location(38.8703041, -77.3210866228, 0)
        self.sda_converter.set_waypoint(test_waypoint)
        self.sda_converter.avoid_obstacles()
        distance = VectorMath.get_magnitude(numpy.array([0,0,0]),self.sda_converter.current_path[0])

        self.assertEqual(self.sda_converter.get_distance_to_current_guided_waypoint(),distance)

    def test_has_path_changed(self):
        path1 = numpy.array([numpy.array([1,2,3]), numpy.array([2,2,3])])
        path2 = numpy.array([numpy.array([1,2,3]), numpy.array([2,2,3]),numpy.array([3,2,3])])
        path3 = numpy.array([numpy.array([1,2,3]), numpy.array([2,2,3]),numpy.array([4,2,4])])
        path4 = numpy.array([numpy.array([1,2,3]), numpy.array([2,2,3]),numpy.array([400,2,4])])

        self.assertTrue(self.sda_converter.has_path_changed(path1,path2))
        self.assertEqual(False,self.sda_converter.has_path_changed(path2,path3))
        self.assertTrue(self.sda_converter.has_path_changed(path2,path4))

    def test_is_obstacle_in_path(self):
        self.sda_converter.obstacle_map.add_waypoint(numpy.array([90,0,0]))
        self.sda_converter.obstacle_map.add_obstacle(StationaryObstacle(numpy.array([40,0,0]),5,100))
        self.sda_converter.set_uav_position(self.initial_coordinates)

        self.assertTrue(self.sda_converter.is_obstacle_in_path())

    def test_set_waypoints(self):
        test_waypoint = Location(38.8742103, -77.3217697, 91.44000244140625)
        self.sda_converter.set_waypoint(test_waypoint)
        obstacle_map = self.sda_converter.obstacle_map
        waypoint_holder = obstacle_map.drone.get_waypoint_holder()
        new_gps_point = inverse_haversine(self.sda_converter.initial_coordinates, [waypoint_holder[0][0], waypoint_holder[0][1], 91.44000244140625])

        self.assertTrue(abs(new_gps_point.get_lat() - test_waypoint.get_lat()) < 0.004)
        self.assertTrue(abs(new_gps_point.get_lon() - test_waypoint.get_lon()) < 0.004)

    def test_add_obstacle(self):
        new_obstacle = interop.StationaryObstacle(38.8703041, -77.3214035, 0, 60.950000762939453)
        self.sda_converter.add_obstacle(Location(38.8703041, -77.3214035, 60.950000762939453), new_obstacle)
       
        self.assertEqual(self.sda_converter.obstacle_map.get_obstacles()[0].get_radius(), new_obstacle.cylinder_radius+30)

    def test_reset_obstacles(self):
        self.assertEqual(self.sda_converter.obstacle_map.obstacles.size,0)

        self.sda_converter.obstacle_map.add_obstacle(numpy.array([10, 10, 10]))
        self.sda_converter.reset_obstacles()
        obstacle_map = self.sda_converter.obstacle_map

        self.assertEqual(obstacle_map.obstacles.size, 0)

    def test_set_uav_position(self):
        new_location = Location (40, -80, 95)
        self.sda_converter.set_uav_position(new_location)

        converted_uav_location = convert_to_point(self.initial_coordinates, new_location)

        self.assertTrue(numpy.array_equal(self.sda_converter.obstacle_map.drone.point, converted_uav_location))