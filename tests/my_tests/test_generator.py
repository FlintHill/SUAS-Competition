from MovingObstacleSimulator import *
import unittest
import numpy

class TestGenerator (unittest.TestCase):
	def setUp(self):
		self.generator = Generator()

	def test_obstacle_map_generator(self):
		obstacle_map1 = self.generator.generate_obstacle_map()

	def test_obstacle_generator(self):
		self.generator.reset_intervalues()
		self.generator.generate_obstacle_map()
		self.generator.generate_stationary_obstacle()
		

	def test_generate_moving_obstacle_values(self):
		self.generator.reset_intervalues()
		self.generator.generate_obstacle_map()
		point, radius, velocity = self.generator.generate_moving_obstacle_values()
		tr = self.generator.top_right_boundary_point 
		tl = self.generator.top_left_boundary_point
		bl = self.generator.bottom_left_boundary_point
		br = self.generator.bottom_right_boundary_point
		# print(tr)
		# print(tl)
		# print(bl)
		# print(br)
		# print("===============================================================")
		# print(point)
		# print(radius)
		# print(velocity)

	def test_generator_add_sationary_obstacle(self):
		self.generator.reset_intervalues()
		obstalce_map = self.generator.generate_obstacle_map()
		obstacle1 = self.generator.add_stationary_obstacle(obstalce_map, 2)

	def test_movement_method(self):
		self.generator.reset_intervalues()
		obstalce_map = self.generator.generate_obstacle_map()
		self.generator.add_stationary_obstacle(obstalce_map,2)
		for obstacle in obstalce_map.obstacles:
			print(obstacle.point)
			print(obstacle.radius)
		obstalce_map.add_waypoint(self.generator.top_right_boundary_point)
		obstalce_map.update_repulsive_forces()
		obstalce_map.update_attractive_force()
		# avoidance_vector = obstalce_map.get_avoidance_vector()
		# print(avoidance_vector)
		# unit_velocity = VectorMath.get_unit_vector(avoidance_vector)
		# print(unit_velocity)