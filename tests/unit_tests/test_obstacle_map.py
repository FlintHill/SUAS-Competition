from SDA import *
import unittest
import numpy

class TestObstacleMap(unittest.TestCase):

	def setUp(self):
		self.test_drone_point = numpy.array([200, 200, 2])
		self.test_fly_zones = numpy.array([numpy.array([(-400, -400),  (-400, 300),  (300, 300),  (300, -400)])])
		self.test_drone_point2 = numpy.array([300, 300, 100])
		self.test_fly_zones2 = numpy.array([numpy.array([(0, 0), (0, 1000), (1000, 1000), (1000, 0)])])
		self.test_drone_point3 = numpy.array([960, 960, 960])
		self.test_drone_point4 = numpy.array([50, 50, 960])
		self.test_drone_point5 = numpy.array([150, 150, 150])
		self.obstacle_map1 = ObstacleMap(self.test_drone_point, self.test_fly_zones)
		self.obstacle_map2 = ObstacleMap(self.test_drone_point2, self.test_fly_zones2)
		self.obstacle_map3 = ObstacleMap(self.test_drone_point3, self.test_fly_zones2)

	def test_add_obstacle(self):
		"""
		 test if the last obstacle in obstacle_map is the added object
		"""

		self.test_obstacle = StationaryObstacle(numpy.array([1, 1, 1]), 2, 1)
		self.obstacle_map1.add_obstacle(self.test_obstacle)
		self.assertEqual(self.obstacle_map1.get_obstacles(), self.test_obstacle)

		self.obstacle_map1.reset_obstacles()
		self.obstacle_map1.reset_waypoints()

		self.test_obstacle1 = StationaryObstacle(numpy.array([1, 1, 1]), 1, 1)
		self.obstacle_map1.add_obstacle(self.test_obstacle)
		self.obstacle_map1.add_obstacle(self.test_obstacle1)
		test_point = self.obstacle_map1.get_obstacles()[0].get_point()
		self.assertTrue(numpy.array_equal(test_point, [1, 1, 1]))

		self.obstacle_map1.reset_obstacles()
		self.obstacle_map1.reset_waypoints()

		self.test_obstacle2 = StationaryObstacle(numpy.array([100, 100, 10]), 2, 1)
		self.test_obstacle3 = StationaryObstacle(numpy.array([-100, -100, 10]), 2, 1)
		self.obstacle_map1.add_obstacle(self.test_obstacle)
		self.obstacle_map1.add_obstacle(self.test_obstacle2)
		self.obstacle_map1.add_obstacle(self.test_obstacle3)
		test_array = numpy.array([self.test_obstacle, self.test_obstacle2, self.test_obstacle3])
		self.assertTrue(numpy.array_equal(self.obstacle_map1.get_obstacles(), test_array))

		self.obstacle_map1.reset_obstacles()
		self.obstacle_map1.reset_waypoints()

		self.test_obstacle4 = StationaryObstacle(numpy.array([0, 0, 10]), 10, 3)
		self.test_obstacle5 = StationaryObstacle(numpy.array([50, 50, 10]), 10, 4)
		test_array1 = numpy.array([25.0, 25.0, 10.0])
		self.obstacle_map1.add_obstacle(self.test_obstacle4)
		self.obstacle_map1.add_obstacle(self.test_obstacle5)
		self.assertTrue(numpy.array_equal(self.obstacle_map1.get_obstacles()[0].get_point(), test_array1))

		self.obstacle_map1.reset_obstacles()
		self.obstacle_map1.reset_waypoints()

		self.test_obstacle6 = StationaryObstacle(numpy.array([-100, -100, 10]), 10, 3)
		self.test_obstacle7 = StationaryObstacle(numpy.array([-150, -150, 10]), 10, 4)
		test_array2 = numpy.array([-125.0, -125.0, 10.0])
		self.obstacle_map1.add_obstacle(self.test_obstacle6)
		self.obstacle_map1.add_obstacle(self.test_obstacle7)
		self.assertTrue(numpy.array_equal(self.obstacle_map1.get_obstacles()[0].get_point(), test_array2))

	def test_add_waypoint(self):
		"""
		test if the last waypoint in waypoint_holder is the added way point
		"""

		self.new_waypoint = numpy.array([1, 1, 1])
		self.obstacle_map1.add_waypoint(self.new_waypoint)
		self.added_waypoint = self.obstacle_map1.get_drone().get_waypoint_holder().get_current_waypoint()
		self.assertEqual(self.added_waypoint.all(), self.new_waypoint.all())

		self.obstacle_map1.reset_obstacles()
		self.obstacle_map1.reset_waypoints()

		self.new_waypoint1 = numpy.array([3, 3, 3])
		self.obstacle_map1.add_waypoint(self.new_waypoint)
		self.obstacle_map1.add_waypoint(self.new_waypoint1)
		self.added_waypoint = self.obstacle_map1.get_drone().get_waypoint_holder()[0]
		self.added_waypoint1 = self.obstacle_map1.get_drone().get_waypoint_holder()[1]
		self.assertEqual(self.added_waypoint.all(), self.new_waypoint.all())
		self.assertEqual(self.added_waypoint1.all(), self.new_waypoint1.all())

	def test_set_drone_position(self):
		"""
		set drone to a new position and check if drone's current position has changed into the new point
		"""

		self.new_point = numpy.array([2, 2, 2])
		self.obstacle_map1.set_drone_position(self.new_point)
		self.assertEqual(self.obstacle_map1.get_drone().get_point().all(), self.new_point.all())

	def test_reset_obstacles(self):
		self.test_obstacle = StationaryObstacle(numpy.array([1, 1, 1]), 2, 1)
		self.obstacle_map1.add_obstacle(self.test_obstacle)
		self.obstacle_map1.reset_obstacles()
		self.assertEqual(len(self.obstacle_map1.get_obstacles()), 0)

	def test_reset_waypoint(self):
		"""
		add,  rest then test if there is any waypoint
		"""
		self.obstacle_map1.reset_waypoints()
		self.assertEqual(self.obstacle_map1.get_drone().get_waypoint_holder().__len__(), 0)

	def test_is_obstacle_in_path(self):

		"""
		reset the obstacle list first,  given a new point and check the return value
		according to the current value,  the obstacle should be in path so the return value should be true
		"""
		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.reset_obstacles()
		self.obstacle_map1.set_drone_position(numpy.array([0,0,0]))
		self.obstacle_in_path = StationaryObstacle(numpy.array([0, 50, 0]), 5, 20)
		self.obstacle_map1.add_obstacle(self.obstacle_in_path)
		self.obstacle_map1.add_waypoint(numpy.array([0, 100, 0]))
		obstacle_in_path_boolean, avoid_paths = self.obstacle_map1.is_obstacle_in_path()
		self.assertEqual(obstacle_in_path_boolean, True)

		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.reset_obstacles()
		self.obstacle_map1.set_drone_position(numpy.array([0,0,0]))
		self.obstacle_in_path1 = StationaryObstacle(numpy.array([50, 50, 0]), 5, 20)
		self.obstacle_map1.add_obstacle(self.obstacle_in_path1)
		self.obstacle_map1.add_waypoint(numpy.array([100, 100, 0]))
		obstacle_in_path_boolean1, avoid_paths1 = self.obstacle_map1.is_obstacle_in_path()
		self.assertEqual(obstacle_in_path_boolean1, True)

		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.reset_obstacles()
		self.obstacle_map1.set_drone_position(numpy.array([0,0,0]))
		self.obstacle_in_path2 = StationaryObstacle(numpy.array([-150, -150, 0]), 5, 20)
		self.obstacle_map1.add_obstacle(self.obstacle_in_path2)
		self.obstacle_map1.add_waypoint(numpy.array([-200, -200, 0]))
		obstacle_in_path_boolean2, avoid_paths2 = self.obstacle_map1.is_obstacle_in_path()
		self.assertEqual(obstacle_in_path_boolean2, True)

		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.reset_obstacles()
		self.obstacle_map1.add_waypoint(numpy.array([20, 20, 2]))
		self.obstacle_map1.set_drone_position(numpy.array([0,0,0]))
		self.obstacle_in_path = StationaryObstacle(numpy.array([30, 30, 1]), 5, 20)
		self.obstacle_map1.add_obstacle(self.obstacle_in_path)
		self.assertEqual(self.obstacle_map1.is_obstacle_in_path(), (False, None))

	def test_generate_possible_path(self):
		"""
		 resect the obstacle list first
		 save an obstacle into the obstacles
		 generate new path
		 check if the obstacel is in the new path
 		"""
		self.obstacle_map1.reset_obstacles()
		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.set_drone_position(numpy.array([0,0,0]))
		self.obstacle_map1.add_waypoint(numpy.array([100, 100, 2]))
		self.test_obstacle = StationaryObstacle(numpy.array([150, 150, 1]), 10, 300)
		#self.test_waypoint = numpy.array([100, 100, 2])
		#self.test_waypoint2 = numpy.array([600, 800, 700])
		self.attempt_paths = self.obstacle_map1.generate_possible_paths(self.test_obstacle)

		for paths in self.attempt_paths:
			self.assertTrue(not self.obstacle_map1.does_path_intersect_obstacle_2d(self.test_obstacle, self.attempt_paths[0][0], self.attempt_paths[0][1]))
			print (paths)

	def test_get_obstacles(self):
		self.obstacle_map1.reset_obstacles()
		self.test_obstacle = StationaryObstacle(numpy.array([150, 150, 2]), 10, 300)
		self.test_obstacle2 = StationaryObstacle(numpy.array([150, 150, 2]), 10, 300)
		self.test_obstacle3 = StationaryObstacle(numpy.array([150, 150, 2]), 10, 300)
		self.obstacle_map1.add_obstacle(self.test_obstacle)
		self.obstacle_map1.add_obstacle(self.test_obstacle2)
		self.obstacle_map1.add_obstacle(self.test_obstacle3)
		self.point = self.obstacle_map1.get_obstacles()[0].get_point()
		self.assertTrue(numpy.array_equal(self.point, numpy.array([150, 150, 2])))

	def test_has_uav_reached_current_waypoint(self):
		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.add_waypoint(numpy.array([50, 50, 50]))

		self.obstacle_map1.set_drone_position(numpy.array([50, 50, 50]))
		self.assertTrue(self.obstacle_map1.get_drone().has_reached_waypoint())

	def test_does_uav_intersect_obstacle_vertically(self):
		self.test_obstacle = StationaryObstacle(numpy.array([150, 150, 2]), 10, 300)
		self.drone_point = numpy.array([150, 150, 2])
		self.test_waypoint = numpy.array([180, 180, 2])
		self.assertTrue(self.obstacle_map1.does_uav_intersect_obstacle_vertically(self.test_obstacle, self.drone_point, self.test_waypoint))

		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.reset_obstacles()

		self.test_obstacle1 = StationaryObstacle(numpy.array([150, 150, 2]), 10, 10)
		self.drone_point1 = numpy.array([50, 50, 50])
		self.test_waypoint1 = numpy.array([80, 80, 50])
		self.assertFalse(self.obstacle_map1.does_uav_intersect_obstacle_vertically(self.test_obstacle1, self.drone_point1, self.test_waypoint1))

	def test_does_path_intersect_obstacle_2d(self):
		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.reset_obstacles()
		self.test_obstacle = StationaryObstacle(numpy.array([150, 150, 2]), 10, 300)
		self.drone_point = numpy.array([150, 150, 2])
		self.test_waypoint = numpy.array([180, 180, 2])
		self.assertTrue(self.obstacle_map1.does_path_intersect_obstacle_2d(self.test_obstacle, self.drone_point, self.test_waypoint))

		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.reset_obstacles()

		self.test_obstacle1 = StationaryObstacle(numpy.array([-170, -170, 2]), 5, 20)
		self.drone_point1 = numpy.array([0, 0, 2])
		self.test_waypoint1 = numpy.array([-20, -20, 2])
		self.obstacle_map1.set_drone_position(self.drone_point1)
		self.obstacle_map1.add_waypoint(self.test_waypoint1)
		self.obstacle_map1.add_obstacle(self.test_obstacle1)
		self.assertFalse(self.obstacle_map1.does_path_intersect_obstacle_2d(self.test_obstacle1, self.drone_point1, self.test_waypoint1))

		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.reset_obstacles()

		self.test_obstacle2 = StationaryObstacle(numpy.array([170, 170, 2]), 5, 20)
		self.drone_point2 = numpy.array([0, 0, 2])
		self.test_waypoint2 = numpy.array([-20, -20, 2])
		self.obstacle_map1.set_drone_position(self.drone_point2)
		self.obstacle_map1.add_waypoint(self.test_waypoint2)
		self.obstacle_map1.add_obstacle(self.test_obstacle2)
		self.assertFalse(self.obstacle_map1.does_path_intersect_obstacle_2d(self.test_obstacle2, self.drone_point2, self.test_waypoint2))

		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.reset_obstacles()

		self.test_obstacle3 = StationaryObstacle(numpy.array([-170, -170, 2]), 5, 20)
		self.drone_point3 = numpy.array([0, 0, 2])
		self.test_waypoint3 = numpy.array([20, 20, 2])
		self.obstacle_map1.set_drone_position(self.drone_point3)
		self.obstacle_map1.add_waypoint(self.test_waypoint3)
		self.obstacle_map1.add_obstacle(self.test_obstacle3)
		self.assertFalse(self.obstacle_map1.does_path_intersect_obstacle_2d(self.test_obstacle3, self.drone_point3, self.test_waypoint3))

	def test_is_obstacle_in_path_of_drone(self):
		self.obstacle_map1.reset_obstacles()
		self.test_obstacle = StationaryObstacle(numpy.array([-100, -100, 1]), 20, 10)
		self.test_obstacle1 = StationaryObstacle(numpy.array([100, -100, 1]), 20, 10)
		self.obstacle_map1.add_obstacle(self.test_obstacle)
		self.obstacle_map1.add_obstacle(self.test_obstacle1)
		self.assertTrue(self.obstacle_map1.is_obstacle_in_path_of_drone(numpy.array([-100, -100, 2]), numpy.array([-170, -170, 2]), self.test_obstacle))
		self.assertFalse(self.obstacle_map1.is_obstacle_in_path_of_drone(numpy.array([-100, 100, 2]), numpy.array([-170, -170, 2]), self.test_obstacle))
		self.assertTrue(self.obstacle_map1.is_obstacle_in_path_of_drone(numpy.array([100, -100, 2]), numpy.array([170, -170, 2]), self.test_obstacle))

	def test_get_min_path(self):
		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.reset_obstacles()
		self.test_obstacle = StationaryObstacle(numpy.array([50, 50, 2]), 10, 30)
		self.drone_point = numpy.array([0, 0, 2])
		self.test_waypoint = numpy.array([100, 100, 2])
		self.obstacle_map1.add_waypoint(self.test_waypoint)
		self.obstacle_map1.set_drone_position(self.drone_point)
		self.obstacle_map1.add_obstacle(self.test_obstacle)
		self.paths = self.obstacle_map1.generate_possible_paths(self.test_obstacle)
		self.assertTrue(numpy.array_equal(self.obstacle_map1.get_min_path(self.paths), numpy.array([[10, 10, 2], [90, 10, 2]])))

		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.reset_obstacles()
		self.test_obstacle1 = StationaryObstacle(numpy.array([0, 50, 2]), 10, 30)
		self.drone_point1 = numpy.array([0, 0, 2])
		self.test_waypoint1 = numpy.array([0, 100, 2])
		self.obstacle_map1.add_waypoint(self.test_waypoint1)
		self.obstacle_map1.set_drone_position(self.drone_point1)
		self.obstacle_map1.add_obstacle(self.test_obstacle1)
		self.paths1 = self.obstacle_map1.generate_possible_paths(self.test_obstacle1)
		self.assertTrue(numpy.array_equal(self.obstacle_map1.get_min_path(self.paths1), numpy.array([[-40, 10, 2], [-40, 90, 2]])))

	def test_generate_possible_paths(self):
		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.reset_obstacles()
		self.test_obstacle = StationaryObstacle(numpy.array([50, 50, 2]), 10, 30)
		self.drone_point = numpy.array([0, 0, 2])
		self.test_waypoint = numpy.array([100, 100, 2])
		self.obstacle_map1.add_waypoint(self.test_waypoint)
		self.obstacle_map1.set_drone_position(self.drone_point)
		self.obstacle_map1.add_obstacle(self.test_obstacle)
		self.paths = self.obstacle_map1.generate_possible_paths(self.test_obstacle)
		self.correct_values = self.obstacle_map1.generate_possible_paths(self.test_obstacle)
		self.assertTrue(numpy.array_equal(self.paths, self.correct_values))

		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.reset_obstacles()
		self.test_obstacle1 = StationaryObstacle(numpy.array([0, 50, 2]), 10, 30)
		self.drone_point1 = numpy.array([0, 0, 2])
		self.test_waypoint1 = numpy.array([0, 100, 2])
		self.obstacle_map1.add_waypoint(self.test_waypoint1)
		self.obstacle_map1.set_drone_position(self.drone_point1)
		self.obstacle_map1.add_obstacle(self.test_obstacle1)
		self.paths1 = self.obstacle_map1.generate_possible_paths(self.test_obstacle1)
		self.correct_values1 = self.obstacle_map1.generate_possible_paths(self.test_obstacle1)
		self.assertTrue(numpy.array_equal(self.paths1, self.correct_values1))

		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.reset_obstacles()
		self.test_obstacle2 = StationaryObstacle(numpy.array([0, -50, 2]), 10, 30)
		self.drone_point2 = numpy.array([0, 0, 2])
		self.test_waypoint2 = numpy.array([0, -100, 2])
		self.obstacle_map1.add_waypoint(self.test_waypoint2)
		self.obstacle_map1.set_drone_position(self.drone_point2)
		self.obstacle_map1.add_obstacle(self.test_obstacle2)
		self.paths2 = self.obstacle_map1.generate_possible_paths(self.test_obstacle2)
		self.correct_values2 = self.obstacle_map1.generate_possible_paths(self.test_obstacle2)
		self.assertTrue(numpy.array_equal(self.paths2, self.correct_values2))

		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.reset_obstacles()
		self.test_obstacle3 = StationaryObstacle(numpy.array([50, 20, 2]), 10, 30)
		self.drone_point3 = numpy.array([0, 0, 2])
		self.test_waypoint3 = numpy.array([100, 0, 2])
		self.obstacle_map1.add_waypoint(self.test_waypoint3)
		self.obstacle_map1.set_drone_position(self.drone_point3)
		self.obstacle_map1.add_obstacle(self.test_obstacle3)
		self.paths3 = self.obstacle_map1.generate_possible_paths(self.test_obstacle3)
		self.correct_values3 = self.obstacle_map1.generate_possible_paths(self.test_obstacle3)
		self.assertTrue(numpy.array_equal(self.paths3, self.correct_values3))

		self.test_drone_point2 = numpy.array([0, 0, 2])
		self.test_fly_zones2 = numpy.array([numpy.array([(-100, -100),  (-100, 100),  (200, 100),  (200, -100)])])
		self.obstacle_map2 = ObstacleMap(self.test_drone_point2, self.test_fly_zones2)
		self.test_waypoint4 = numpy.array([80, 0, 2])
		self.obstacle_map2.add_waypoint(self.test_waypoint4)
		self.test_obstacle4 = StationaryObstacle(numpy.array([30, -30, 2]), 10, 30)
		self.obstacle_map2.add_obstacle(self.test_obstacle4)
		self.paths4 = self.obstacle_map2.generate_possible_paths(self.test_obstacle4)
		self.correct_values4 = self.obstacle_map2.generate_possible_paths(self.test_obstacle4)
		self.assertTrue(numpy.array_equal(self.paths4, self.correct_values4))

	def test_get_path_distance(self):
		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.reset_obstacles()
		self.test_obstacle = StationaryObstacle(numpy.array([50, 50, 2]), 10, 30)
		self.drone_point = numpy.array([0, 0, 2])
		self.test_waypoint = numpy.array([100, 100, 2])
		self.obstacle_map1.add_waypoint(self.test_waypoint)
		self.obstacle_map1.set_drone_position(self.drone_point)
		self.obstacle_map1.add_obstacle(self.test_obstacle)
		self.paths = self.obstacle_map1.generate_possible_paths(self.test_obstacle)
		self.min_path = self.obstacle_map1.get_min_path(self.paths)
		self.assertEqual(self.obstacle_map1.get_path_distance(self.min_path), 184.69598700510511)

		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.reset_obstacles()
		self.test_obstacle1 = StationaryObstacle(numpy.array([-70, -70, 2]), 10, 30)
		self.drone_point1 = numpy.array([0, 0, 2])
		self.test_waypoint1 = numpy.array([-140, -140, 2])
		self.obstacle_map1.add_waypoint(self.test_waypoint1)
		self.obstacle_map1.set_drone_position(self.drone_point1)
		self.obstacle_map1.add_obstacle(self.test_obstacle1)
		self.paths1 = self.obstacle_map1.generate_possible_paths(self.test_obstacle1)
		self.min_path1 = self.obstacle_map1.get_min_path(self.paths1)
		self.assertEqual(self.obstacle_map1.get_path_distance(self.min_path1), 236.44394938110665)

	def test_obstacle_further_than_waypoint(self):
		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.reset_obstacles()

		test_obstacle = StationaryObstacle(numpy.array([200, 200, 10]), 10, 30)
		test_waypoint = numpy.array([50, 50, 0])
		drone_point = numpy.array([0, 0, 0])

		self.obstacle_map1.add_waypoint(test_waypoint)
		self.obstacle_map1.add_obstacle(test_obstacle)
		self.obstacle_map1.set_drone_position(drone_point)

		obstacle_in_path_boolean, avoidance_points = self.obstacle_map1.is_obstacle_in_path()
		self.assertEqual(obstacle_in_path_boolean, False)
