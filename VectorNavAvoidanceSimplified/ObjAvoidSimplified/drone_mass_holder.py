class DroneMassHolder(object):

    def __init__(self, drone_mass):
        self.drone_mass = drone_mass

    def get_drone_mass(self):
        return self.drone_mass

    def set_drone_position(self, new_drone_location):
        self.drone_mass.set_point(new_drone_location)
