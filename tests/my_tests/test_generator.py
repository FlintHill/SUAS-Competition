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