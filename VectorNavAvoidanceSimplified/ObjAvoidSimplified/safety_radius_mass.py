'''
Created on Feb 17, 2017

@author: vtolpegin
'''
from ObjAvoidSimplified import *
import random
import math

class SafetyRadiusMass(Mass):

    def __init__(self, starting_point, mass, safety_radius):
        super(SafetyRadiusMass, self).__init__(starting_point, mass)

        self.safety_radius = safety_radius

        self.radiusCircle = Circle(Point(int(self.point[0] + Window.CENTERPOINT[0]), int(Window.CENTERPOINT[1] - self.point[1])), self.safety_radius)
        self.radiusCircle.setFill("blue")

    def get_required_mass_to_balance_motion(self, drone_mass):
        grav_unit_vector = VectorMath.get_unit_vector(self.get_point(), drone_mass.get_point())
        velocity_vector = drone_mass.get_velocity_vector()
        projection_vector = VectorMath.get_vector_projection(grav_unit_vector, velocity_vector)
        projection_magnitude = VectorMath.get_vector_magnitude(projection_vector)
        mass = (projection_magnitude * self.safety_radius**2) / (Constants.GRAVITATIONAL_CONSTANT * Constants.REFRESH_RATE)

        return mass

    def get_safety_radius(self):
        return self.safety_radius

    def update_mass(self, drone_mass):
        self.set_mass(self.get_required_mass_to_balance_motion(drone_mass))

    def draw(self, win):
        self.radiusCircle.draw(win.getGraphWin())
        super(SafetyRadiusMass, self).draw(win)
