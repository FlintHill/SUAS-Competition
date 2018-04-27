from SDAWithVectorField import *
import numpy
import math

class MovementMethods(object):
	
	def __init__(self):
		pass

	@staticmethod
	def drone_move(self, obstacel_map):
		"""
		need testing
		"""
		unit_velocity = VectorMath.get_unit_vector(obstacle_map.get_avoidance_vector)
		while obstacle_map.drone.waypoint_holder.reached_current_waypoint(obstacle_map.drone.point) == False:
			obstacle_map.set_drone_position(numpy.array([obstacle_map.drone.point[0]+unit_velocity[0], obstacle_map.drone.point[1]+unit_velocity[1]]))



