from SDAWithVectorField import *
import unittest
import numpy

class TestObstacleMap(unittest.TestCase):
	def setUp(self):
		self.test_drone_point = numpy.array([0, 0, 0])
		self.test_fly_zones = numpy.array([numpy.array([(-400, -400),  (-400, 300),  (300, 300),  (300, -400)])])
		self.test_drone_point2 = numpy.array([300, 300, 100])
		self.test_fly_zones2 = numpy.array([numpy.array([(0, 0), (0, 1000), (1000, 1000), (1000, 0)])])
		self.test_drone_point3 = numpy.array([20, 20, 20])
		self.test_drone_point4 = numpy.array([500, 500, 20])
		self.test_drone_point5 = numpy.array([15, 150, 150])
		self.obstacle_map1 = ObstacleMap(self.test_drone_point, self.test_fly_zones)
		self.obstacle_map2 = ObstacleMap(self.test_drone_point2, self.test_fly_zones2)
		self.obstacle_map3 = ObstacleMap(self.test_drone_point3, self.test_fly_zones2)
		self.obstacle1 = MovingObstacle(numpy.array([50,50,50]), 10)
		self.obstacle2 = MovingObstacle(numpy.array([200,200,200]), 10)
		self.waypoint = numpy.array([100,100,100])
	
	def test_add_forces(self):
		self.obstacle_map1.reset_obstacles()
		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.reset_attractive_force()
		self.obstacle_map1.reset_repulsive_forces()
		self.obstacle_map1.set_drone_position(self.test_drone_point)
		self.obstacle_map1.add_obstacle(self.obstacle1)
		self.obstacle_map1.add_obstacle(self.obstacle2)

		initial_force = numpy.array([0,0,0])
		repulsive_force1 = VectorMath.get_force(self.obstacle_map1.drone.point, self.obstacle1.get_point())
		repulsive_force2 = VectorMath.get_force(self.obstacle_map1.drone.point, self.obstacle2.get_point())

		self.obstacle_map1.add_force()

		sum_of_forces = numpy.sum([repulsive_force1, repulsive_force2], axis= 0)

		self.assertEqual(self.obstacle_map1.repulsive_forces[0], sum_of_forces[0])
		self.assertEqual(self.obstacle_map1.repulsive_forces[1], sum_of_forces[1])
		self.assertEqual(self.obstacle_map1.repulsive_forces[2], sum_of_forces[2])

	def test_set_attractive_force(self):
		self.obstacle_map1.reset_obstacles()
		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.reset_attractive_force()
		self.obstacle_map1.reset_repulsive_forces()
		self.obstacle_map1.set_drone_position(self.test_drone_point)
		self.obstacle_map1.add_waypoint(self.waypoint)
		self.obstacle_map1.set_attractive_force()

		attractive_force = VectorMath.get_force(self.test_drone_point, self.waypoint)

		self.assertEqual(self.obstacle_map1.get_attractive_force()[0], attractive_force[0])
		self.assertEqual(self.obstacle_map1.get_attractive_force()[1], attractive_force[1])
		self.assertEqual(self.obstacle_map1.get_attractive_force()[2], attractive_force[2])


	def test_get_avoidance_vector(self):
		self.obstacle_map1.reset_obstacles()
		self.obstacle_map1.reset_waypoints()
		self.obstacle_map1.reset_attractive_force()
		self.obstacle_map1.reset_repulsive_forces()
		self.obstacle_map1.add_obstacle(self.obstacle1)
		self.obstacle_map1.add_waypoint(self.waypoint)
		self.obstacle_map1.add_force()
		self.obstacle_map1.set_attractive_force()
		result = self.obstacle_map1.get_avoidance_vector()

		repulsive_forces = VectorMath.get_force(self.test_drone_point, self.obstacle1.get_point())
		attractive_force = VectorMath.get_force(self.test_drone_point, self.waypoint)
		avoidance_vector = numpy.sum([attractive_force, repulsive_forces], axis=0)

		self.assertEqual(result[0], avoidance_vector[0])
		


