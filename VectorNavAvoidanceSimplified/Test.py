'''
Created on Feb 18, 2017

@author: vtolpegin
'''
import random
import numpy as np
from time import sleep
from ObjAvoidSimplified import *

class Test:

    def __init__(self):
        mass_holder = MassHolder([])
        drone_mass = DroneMass(10, get_random_points_in_bounds(2, 10, ((-500,500), (-200,200))))
        random_masses = self.generate_random_masses(50)
        for random_mass in random_masses:
            mass_holder.append_mass(random_mass)

        self.map = Map(mass_holder, drone_mass)
        self.window = Window(self.map, (1440,900))

    def generate_random_masses(self, number_masses):
        masses = []
        random_masses = get_random_points_in_bounds(2, number_masses, ((-720,720), (-450,450)))
        for i in range(0, len(random_masses)):
            masses.append(SafetyRadiusMass(random_masses[i], 500, 20))

        return masses

if __name__ == '__main__':
    my_test = Test()
