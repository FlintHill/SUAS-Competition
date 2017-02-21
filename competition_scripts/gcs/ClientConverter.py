'''
Created on Feb 20, 2017

@author: phusisian
@author: vtolpegin
'''
from ObjAvoidSimplified import *
from current_coordinates import CurrentCoordinates
from math import sin, cos, atan2
from static_math import *

class ClientConverter(object):

    '''initialCoordinates will be CurrentCoordinates object'''
    '''the role of the class is to funnel data from the client script into forms that are usable with my code.
    currently updates the position of the drone mass, but is set up to update other masses as well if it were
    to be funneled them fairly simply'''
    def __init__(self, initial_coordinates):
        mass_holder = MassHolder([])
        drone_mass = DroneMass(10, get_random_points_in_bounds(2, 10, ((-500,500), (-200,200))))
        random_masses = self.generate_random_masses(50)
        for random_mass in random_masses:
            mass_holder.append_mass(random_mass)
        self.map = Map(mass_holder, drone_mass)

        self.initial_coordinates = initial_coordinates

    def get_initial_coordinates(self):
        return self.initial_coordinates

    '''pass waypoint list from here. Shouldn't need to be updated afterward.'''
    def set_waypoints(self, new_waypoints):
        for waypoint in new_waypoints:
            converted_waypoint = waypoint.convert_to_point(self.get_initial_coordinates())

            self.map.add_waypoint(converted_waypoint)

    def generate_random_masses(self, number_masses):
        masses = []
        random_masses = get_random_points_in_bounds(2, number_masses, ((-720,720), (-450,450)))
        for i in range(0, len(random_masses)):
            masses.append(SafetyRadiusMass(random_masses[i], 500, 20))

        return masses

    '''takes an converter_data_update object that wraps altitude, haversine distance, and heading from the current position
    to the position the drone needs to travel'''
    def update_drone_mass_position(self, update_data):
        dy = update_data.get_haversine_distance() * sin(update_data.get_heading())
        dx = update_data.get_haversine_distance() * cos(update_data.get_heading())
        new_drone_location =  np.array([dx, dy, update_data.get_altitude()])
        self.map.set_drone_location(new_drone_location)
        did_avoid_obstacles = self.mainDroneMass.applyMotions()

        print(self.map)

        if did_avoid_obstacles:
            appliedPoint = self.map.get_drone_location()
            bearing = atan2(appliedPoint[1] / appliedPoint[0])

            return inverse_haversine(self.get_initial_coordinates(), [appliedPoint[0], appliedPoint[1], updateData.get_altitude()], bearing)

        return None
