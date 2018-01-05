from SDA import *
import numpy

class Mass(Object)
	"""
	mass for obstacle avoidance
	"""
	def __init__(self, starting_point, force):
		"""
		:para starting_point: numpy array
		:para force: numpy array
		"""
		self.starting_point = starting_point
		self.force = force

	def get_starting_point(self):
		return self.starting_point

	def get_force(self):
		return self.force



