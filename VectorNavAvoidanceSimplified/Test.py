'''
Created on Feb 18, 2017

@author: vtolpegin
'''
import random
import numpy as np
from ObjAvoidSimplified import *

class Test:

    def __init__(self):
        mass_holder = MassHolder()
        drone_mass_holder = DroneMassHolder(DroneMass(np.array([0,0]), 10))
        random_masses = generate_random_masses(5)
        for random_mass in random_masses:
            mass_holder.append_mass(random_mass)

        self.map = Map(mass_holder, drone_mass_holder)

    def generate_random_masses(self, number_masses):
        masses = []
        random_masses = get_random_points_in_bounds(2, number_masses, ((-50, 50), (-50,50)))
        for i in range(0, len(random_masses)):
            masses.append(SafetyRadiusMass(random_masses[i], 500, 20))

        return masses

    def run_test(self):
        while True:
            self.map.avoid_obstacles()

            print(self.map)

if __name__ == '__main__':
    my_test = Test()
    my_test.run_test()
