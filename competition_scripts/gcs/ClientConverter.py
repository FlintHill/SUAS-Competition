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
        drone_mass = DroneMass(1, np.array([[0, 0]]))
        random_masses = self.generate_random_masses(10)
        for random_mass in random_masses:
            mass_holder.append_mass(random_mass)
        self.map = Map(mass_holder, drone_mass)

        self.initial_coordinates = initial_coordinates

    def get_initial_coordinates(self):
        return self.initial_coordinates

    '''pass waypoint list from here. Shouldn't need to be updated afterward.'''
    def set_waypoints(self, new_waypoints):
        for waypoint in new_waypoints:
            converted_waypoint = np.array([waypoint.convert_to_point(self.get_initial_coordinates())[:-1]])

            print(converted_waypoint)
            self.map.add_waypoint(converted_waypoint)

    def generate_random_masses(self, number_masses):
        masses = []
        random_masses = get_random_points_in_bounds(2, number_masses, ((-100,400), (-150,300)))
        for i in range(0, len(random_masses)):
            masses.append(SafetyRadiusMass(random_masses[i], 500, 5))

        return np.array([SafetyRadiusMass((100, 9), 500, 10)])#np.array(masses)

    def get_map(self):
        return self.map

    def update_drone_mass_position(self, update_data):
        dy = update_data.get_haversine_distance() * sin(update_data.get_heading())
        dx = update_data.get_haversine_distance() * cos(update_data.get_heading())
        new_drone_location =  np.array([dx, dy])#, update_data.get_altitude()])
        self.map.set_drone_location(new_drone_location)

        for obstacle in self.map.get_mass_holder():
            dist = VectorMath.get_magnitude(obstacle.get_point(), self.map.get_drone_mass().get_point())

            if dist < 10:
                print(obstacle)

        print("Before did_avoid_obstacles: " + str(self.map.get_drone_mass()))
        did_avoid_obstacles = self.map.avoid_obstacles()
        for i in range(3):
            self.map.avoid_obstacles()
        print("After did_avoid_obstacles: " + str(self.map.get_drone_mass()))

        if did_avoid_obstacles:
            appliedPoint = self.map.get_drone_location()
            bearing = atan2(appliedPoint[0], appliedPoint[1])

            return inverse_haversine(self.get_initial_coordinates(), [appliedPoint[0], appliedPoint[1], update_data.get_altitude()], bearing)

        return None
