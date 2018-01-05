import numpy
from math import atan2, cos, sin, pi, sqrt
from SDAWithVectorField import *

class ObstacleMap(object):
	def __init__(self, drone_point, fly_zones):
		self.obstacles = numpy.array([])
		self.drone = Drone(drone_point, numpy.array([]))
		self.fly_zones = FlightBoundariesContainer(fly_zones)
		self.repulsive_forces = numpy.array([0,0,0])
		self.attractive_force = numpy.array([0,0,0])
		self.detection_radius = 0

	def add_obstacle(self, obstacle):
		if self.obstacles.size != 0:
			final_obstacles = numpy.hstack([self.obstacles, obstacle])
			self.obstacles = final_obstacles
		else:
			self.obstacles = numpy.array([obstacle])

	def add_force(self):
		for obstacle in self.obstacles:
			if obstacle.get_type() == "moving":
				force = VectorMath.get_force(self.drone.get_point(), obstacle.get_point())
				self.repulsive_forces = numpy.sum([self.repulsive_forces, force], axis=0)

	def set_attractive_force(self):
		self.attractive_force = VectorMath.get_force(self.drone.point, self.drone.waypoint_holder.get_current_waypoint())

	def reset_attractive_force(self):
		self.attractive_force = numpy.array([0,0,0])

	def reset_repulsive_forces(self):
		self.repulsive_forces = numpy.array([0,0,0])

	def get_avoidance_vector(self):
		repulsive_forces = self.repulsive_forces
		attractive_force = self.attractive_force
		avoidance_vector = numpy.sum([attractive_force, repulsive_forces], axis= 0)
		return avoidance_vector

	def get_attractive_force(self):
		return self.attractive_force

	def get_repulsive_forces(self):
		return self.repulsive_forces

	def add_waypoint(self, waypoint):
		"""
        Add a waypoint to the drone

        :param waypoint: The waypoint to add
        :type waypoint: Numpy Array
        """
		self.drone.add_waypoint(waypoint)

	def set_drone_position(self, new_point):
		self.drone.set_drone_position(new_point)

	def reset_obstacles(self):
		self.obstacles = numpy.array([])

	def reset_waypoints(self):
		self.drone.reset_waypoints()
