from SDA import *
import unittest
import numpy

class Test_Obstacle_map(unittest.TestCase):

	def setUp(self):
		self.test_drone_point = numpy.array([200,200,2])
		self.test_fly_zones = numpy.array([numpy.array([(0,0), (0,300), (300,300), (300,0)])])
		self.test_drone_point2 = numpy.array([300,300,100])
		self.test_fly_zones2 = numpy.array([numpy.array([(0,0),(0,1000),(1000,1000),(1000,0)])])
		self.test_drone_point3 = numpy.array([960,960,960])
		self.test_drone_point4 = numpy.array([50,50,960])
		self.test_drone_point5 = numpy.array([150,150,150])
		self.obstacle_map1 = ObstacleMap(self.test_drone_point,self.test_fly_zones)
		self.obstacle_map2 = ObstacleMap(self.test_drone_point2,self.test_fly_zones2)
		self.obstacle_map3 = ObstacleMap(self.test_drone_point3,self.test_fly_zones2)

	def test_add_obstacle(self):
		"""
		 test if the last obstacle in obstacle_map is the added object
		"""

		self.test_obstacle = StationaryObstacle(numpy.array([1,1,1]),2,1)
		self.obstacle_map1.add_obstacle(self.test_obstacle)

		#self.test_obstacle2 = StationaryObstacle(numpy.array([1,1,1]),4,1)
		#self.test_obstacle3 = StationaryObstacle(numpy.array([1,1,1]),2,1)

		self.assertEqual(self.obstacle_map1.get_obstacles(),self.test_obstacle)

	def test_add_waypoint(self):
		"""
		test if the last waypoint in waypoint_holder is the added way point
		"""

		self.new_waypoint = numpy.array([1,1,1])

		self.obstacle_map1.add_waypoint(self.new_waypoint)

		self.added_waypoint = self.obstacle_map1.get_drone().get_waypoint_holder().get_current_waypoint()

		self.assertEqual(self.added_waypoint.all(),self.new_waypoint.all())

	def test_set_drone_position(self):
		"""
		set drone to a new position and check if drone's current position has changed into the new point
		"""

		self.new_point = numpy.array([2,2,2])

		self.obstacle_map1.set_drone_position(self.new_point)

		self.assertEqual(self.obstacle_map1.get_drone().get_point().all(),self.new_point.all())

	def test_reset_obstacles(self):
		self.test_obstacle = StationaryObstacle(numpy.array([1,1,1]),2,1)
		self.obstacle_map1.add_obstacle(self.test_obstacle)
		self.obstacle_map1.reset_obstacles()
		self.assertEqual(len(self.obstacle_map1.get_obstacles()),0)

	def test_reset_waypoint(self):
		"""
		add, rest then test if there is any waypoint
		"""
		self.obstacle_map1.reset_waypoints()
		self.assertEqual(self.obstacle_map1.get_drone().get_waypoint_holder().__len__(),0)

	def test_is_obstacle_in_path(self):

		"""
		reset the obstacle list first, given a new point and check the return value
		according to the current value, the obstacle should be in path so the return value should be true
		"""

		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.add_waypoint(numpy.array([2,2,2]))
		self.assertTrue(self.obstacle_map1.is_obstacle_in_path())


	def test_generate_possible_path(self):
		"""
		 resect the obstacle list first
		 save an obstacle into the obstacles
		 generate new path
		 check if the obstacel is in the new path
 		"""
		self.obstacle_map1.reset_obstacles()
		self.obstacle_map1.add_waypoint(numpy.array([100,100,2]))
		self.test_obstacle = StationaryObstacle(numpy.array([150,150,2]),10,300)
		self.test_waypoint = numpy.array([100,100,2])
		self.test_waypoint2 = numpy.array([600,800,700])
		self.attempt_paths = self.obstacle_map1.generate_possible_paths(self.test_obstacle)

		for paths in self.attempt_paths:
			self.assertTrue(not self.obstacle_map1.does_path_intersect_obstacle_3d(self.test_obstacle,self.attempt_paths[0][0],self.attempt_paths[0][1]))
			print (paths)


	def test_get_obstacles(self):
		self.obstacle_map1.reset_obstacles()
		self.test_obstacle = StationaryObstacle(numpy.array([150,150,2]),10,300)
		self.test_obstacle2 = StationaryObstacle(numpy.array([150,150,2]),10,300)
		self.test_obstacle3 = StationaryObstacle(numpy.array([150,150,2]),10,300)
		self.obstacle_map1.add_obstacle(self.test_obstacle)
		self.obstacle_map1.add_obstacle(self.test_obstacle2)
		self.obstacle_map1.add_obstacle(self.test_obstacle3)
		self.length = len(self.obstacle_map1.get_obstacles())
		self.assertEqual(self.length,3)

	def test_has_uav_reached_current_waypoint(self):
		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.add_waypoint(numpy.array([50,50,50]))

		self.obstacle_map1.set_drone_position(numpy.array([50,50,50]))
		self.assertTrue(self.obstacle_map1.get_drone().has_reached_waypoint())


	def test_does_uav_intersect_obstacle_vertically(self):
		self.test_obstacle = StationaryObstacle(numpy.array([150,150,2]),10,300)
		self.drone_point = numpy.array([150,150,2])
		self.test_waypoint = numpy.array([180,180,2])
		self.assertTrue(self.obstacle_map1.does_uav_intersect_obstacle_vertically(self.test_obstacle,self.drone_point,self.test_waypoint))


	def test_does_path_intersect_obstacle_2d(self):
		self.test_obstacle = StationaryObstacle(numpy.array([150,150,2]),10,300)
		self.drone_point = numpy.array([150,150,2])
		self.test_waypoint = numpy.array([180,180,2])
		self.assertTrue(self.obstacle_map1.does_path_intersect_obstacle_2d(self.test_obstacle,self.drone_point,self.test_waypoint))

	def test_does_path_intersect_obstacle_3d(self):
		self.test_obstacle = StationaryObstacle(numpy.array([150,150,2]),10,300)
		self.drone_point = numpy.array([150,150,2])
		self.test_waypoint = numpy.array([180,180,2])
		self.assertTrue(self.obstacle_map1.does_path_intersect_obstacle_3d(self.test_obstacle,self.drone_point,self.test_waypoint))
