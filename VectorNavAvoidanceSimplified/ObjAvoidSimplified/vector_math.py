import math
import numpy as np

class VectorMath(object):
    """
    Encasuplator class for vector operations
    """

    def __init__(self):
        pass

    @staticmethod
    def get_magnitude(point_one, point_two):
        """
        Returns the distance between two points
        """
        if len(point_one) != len(point_two):
            raise ValueError("Point dimension mismatch")

        diff = np.subtract(point_one, point_two)
        dist = np.linalg.norm(diff)

        return dist

    @staticmethod
    def get_force(mass_one, mass_two, scale):
        """
        Return the gravitational attraction force between the masses. This
        method uses the universal law of gravitation to determine the force
        acting on two masses (G * m1 * m2 / r^2)
        """
        distance = float(VectorMath.get_magnitude(mass_one.get_point(), mass_two.get_point()))
        force = (mass_one.get_mass() * mass_two.get_mass())/(distance**2)

        return force * scale

    @staticmethod
    def get_unit_vector(point_one, point_two):
        """
        Returns the unit vector of two points
        """
        unit_vector = np.subtract(point_two, point_one)/VectorMath.get_magnitude(point_one, point_two)

        return unit_vector

    @staticmethod
    def get_single_unit_vector(point_one):
        """
        Returns the unit vector of a vector
        """
        unit_vector = point_one / VectorMath.get_vector_magnitude(point_one)

        return unit_vector

    @staticmethod
    def get_vector_magnitude(vector):
        """
        Returns the magnitude of the vector
        """
        return np.linalg.norm(vector)

    @staticmethod
    def get_vector_projection(vector_one, vector_two):
        """
        Returns the vector projection between two vectors
        """
        dot_prod = np.dot(vector_one, vector_two)
        mag = VectorMath.get_vector_magnitude(vector_one)

        return vector_one * (dot_prod/(mag**2))

    @staticmethod
    def get_angle_between_unit_vectors(vector_one, vector_two):
        """
        Returns angle between two unit vectors
        """
        dot_prod = np.dot(vector_one, vector_two)

        return math.acos(dot_prod)
