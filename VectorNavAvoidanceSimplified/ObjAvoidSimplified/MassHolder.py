'''
Created on Feb 17, 2017

@author: vtolpegin
'''

class MassHolder:

    GRAVITY_CONSTANT = 5000

    def __init__(self, droneMass):
        self.masses = []
        self.droneMass = droneMass

    def append_mass(self, massIn):
        self.masses.append(massIn)

    def get_drone_mass(self):
        return self.droneMass

    def move_drone(self):
        # TODO : Write this method

    def __getitem__(self, index):
        return self.masses[index]

    def __len__(self):
        return len(self.masses)

    def __repr__(self):
        outString = ""
        for i in range(0, len(self)):
            outString += str(self[i]) + "\n"
        outString += str(self.droneMass) + "\n"
        return outString
