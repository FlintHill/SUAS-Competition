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

	def test_generator_add_sationary_obstacle(self):
		self.generator.reset_intervalues()
		obstalce_map = self.generator.generate_obstacle_map()
		obstacle1 = self.generator.add_stationary_obstacle(obstalce_map, 2)

	def test_movement_method(self):
		self.generator.reset_intervalues()
		obstalce_map = self.generator.generate_obstacle_map()
		self.generator.add_stationary_obstacle(obstalce_map,2)

		obstalce_map.add_waypoint(self.generator.top_right_boundary_point)
		print(obstalce_map.drone.point)
		print(obstalce_map.drone.waypoint_holder.get_current_waypoint())
		obstalce_map.update_repulsive_forces()
		obstalce_map.update_attractive_force()
		# avoidance_vector = obstalce_map.get_avoidance_vector()
		# print(avoidance_vector)
		# unit_velocity = VectorMath.get_unit_vector(avoidance_vector)
		# print(unit_velocity)