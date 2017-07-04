'''
Created on Feb 17, 2017

@author: vtolpegin
'''
from ObjAvoidSimplified import *
import random
import math

class Mass(object):

    def __init__(self, starting_point, mass):
        self.point = starting_point
        self.mass = mass

        self.drawCircle = Circle(Point(int(self.get_point()[0] + Window.CENTERPOINT[0]), int(Window.CENTERPOINT[1] - self.get_point()[1])), 5)
        self.drawCircle.setFill("red")

    def update_mass(self, drone_mass):
        pass

    def get_mass(self):
        return self.mass

    def set_mass(self, new_mass):
        self.mass = new_mass

    def get_point(self):
        return self.point

    def set_point(self, new_point):
        self.point = new_point

    def draw(self, win):
        self.drawCircle.draw(win.getGraphWin())

    def __repr__(self):
        return_string = "Mass at: " + str(self.get_point())
        return return_string
