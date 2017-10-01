from SDA import *
import unittest
import numpy 

class Test_Obstacle_map(unittest.TestCase):
	"""docstring for test_Obstacle_map"""
	
	def setUp(self):
		self.test_drone_point=numpy.array([0,0,0])
		self.test_fly_zones=numpy.array([numpy.array([(0,0), (0,100), (100,100), (100,0)])])
		self.obstacle_map=ObstacleMap(self.test_drone_point,self.test_fly_zones)

	def test_add_obstacle(self):

		# test if the last obstacle in obstacle_map is the added object
		
		self.test_Obstacle=StationaryObstacle(numpy.array([1,1,1]),2,1)
		self.obstacle_map.add_obstacle(self.test_Obstacle)
		
		self.assertEqual(self.obstacle_map.get_obstacles(),self.test_Obstacle)

	def test_add_waypoint(self):

		# test if the last waypoint in waypoint_holder is the added way point

		self.new_waypoint=numpy.array([1,1,1])
		
		self.obstacle_map.add_waypoint(self.new_waypoint)
		
		self.added_waypoint=self.obstacle_map.get_drone().get_waypoint_holder().get_current_waypoint()

		self.assertEqual(self.added_waypoint.all(),self.new_waypoint.all())

	def test_set_drone_position(self):

		# set drone to a new position and check if drone's current position has changed into the new point

		self.new_point=numpy.array([2,2,2])

		self.obstacle_map.set_drone_position(self.new_point)

		self.assertEqual(self.obstacle_map.get_drone().get_point().all(),self.new_point.all())

	def test_reset_obstacles(self):

		# add, reset, then test if there is still any obstcle

		self.test_obstacle=StationaryObstacle(numpy.array([1,1,1]),2,1)
		self.obstacle_map.add_obstacle(self.test_obstacle)
		self.obstacle_map.reset_obstacles()
		self.assertEqual(len(self.obstacle_map.get_obstacles()),0)

	def test_reset_waypoint(self):
		# add, rest then test if there is any waypoint

		self.test_waypoint=numpy.array([1,1,1])
		self.obstacle_map.add_waypoint(self.test_waypoint)
		self.obstacle_map.reset_waypoints()
		self.assertEqual(self.obstacle_map.get_drone().get_waypoint_holder().__len__(),0)

	def test_is_obstacle_in_path(self):

		# reset the obstacle list first, given a new point and check the return value
		# according to the current value, the obstacle should be in path so the return value should be true

		self.obstacle_map.get_drone().reset_waypoint()
		self.obstacle_map.get_drone().add_waypoint(np.array([2,2,2]))
		self.assertTrue(self.obstacle_map.is_obstacle_in_path())


	def test_generate_possible_path(self):

		# resect the obstacle list first
		# save an obstacle into the obstacles
		# generate new path
		# check if the obstacel is in the new path

		self.obstacle_map.reset_obstacles()
		self.test_obstacle=SationaryObstacle(np.array([1,1,1]),1,1)
		self.test_paths=self.obstacle_map.generate_possible_path(test_obstacle)
		for paths in test_paths
			self.assertTure(self.obstacle_map.does_path_intersect_obstacle_3d(self.test_obstacle,paths[0],paths[1]))

	
	# def test_get_obstacles(self):

	#  	result_obstacles= self.obstacle_map.get_obstacles()
	#  	for index in range(len(self.result_obstacles))
	#  	self.assertEqual(self.result_obstacles[index],self.obstacle_map.get_obstacles()[index])

	# def test_has_uav_reached_current_waypoint(self):
		
	# 	self.obstacle_map.reset_waypoints()
	# 	self.obstacle_map.add_waypoint(numpy.array([0,0,0]))
	# 	self.obstacle_map.set_drone_position(numpy.array[0,0,0])
	# 	self.assertTure(self.obstacle_map.get_drone().has_reached_waypoint())

	

	# def test_get_drone(self):

	# # return drone

	# 	obstacle_map.reset_waypoint()
	# 	self.assertEqual(obstacle_map.get_drone(),Drone(np.array([0,0,0]),np.array([])))
	

