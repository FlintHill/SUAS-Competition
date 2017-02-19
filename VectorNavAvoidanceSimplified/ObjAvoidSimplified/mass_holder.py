'''
Created on Feb 17, 2017

@author: vtolpegin
'''

class MassHolder(object):

    GRAVITY_CONSTANT = 5000

    def __init__(self, masses):
        """
        Initialize

        :param masses: The masses to initialize the mass holder with
        """
        self.masses = masses

    def append_mass(self, mass):
        """
        Append a mass to the mass holder

        :param mass: The mass to append to the mass holder
        """
        self.masses.append(mass)

    def update_obstacle_mass(self, drone_mass):
        """
        For all obstacles, update the mass to properly manage the force
        based on the drone's distance to the obstacles

        :param drone_mass: The drone mass to base the updates off of
        """
        for index in range(len(self)):
            self[index].update_mass(drone_mass)

    def draw(self, win):
        for i in range(0, len(self)):
            self[i].draw(win)

    def __getitem__(self, index):
        return self.masses[index]

    def __len__(self):
        return len(self.masses)

    def __repr__(self):
        outString = ""
        for i in range(0, len(self)):
            outString += str(self[i]) + "\n"
        return outString
