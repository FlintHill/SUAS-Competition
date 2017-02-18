from ObjAvoidSimplified import *

class Map(object):
    """
    Wrapper class for a map where obstacles are placed
    """

    def __init__(self, masses, drone_mass):
        """
        Initialize

        :param masses: The masses to initialize the map with
        :param drone_mass: The drone mass for the map
        """
        self.mass_holder = MassHolder(masses)
        self.drone_mass_holder = drone_mass

    def append_mass(self, mass):
        """
        Append a mass to the map

        :param mass: The mass you want to append to the map
        """
        self.mass_holder.append_mass(mass)

    def avoid_obstacles(self):
        """
        Run the map once to avoid obstacles
        """
        # TODO: Run the program once, applying all motions

    def get_drone_location(self):
        """
        Return's the drone mass' current position within the map
        """
        return self.drone_mass_holder.get_drone_mass().get_point()

    def update_drone_location(self, new_drone_location):
        """
        Set the drone's location in the map & update the masses of all of the
        obstacles

        :param new_drone_location: The new location for the drone
        """
        self.drone_mass_holder.set_drone_position(new_drone_location)
        self.mass_holder.update_obstacle_mass(self.drone_mass_holder.get_drone_mass())
