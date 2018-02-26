import math
import numpy as np

class VectorMath(object):
    """
    Encasuplation class for vector operations
    """

    def __init__(self):
        pass

    @staticmethod
    def get_magnitude(vector_one, vector_two):
        """
        Returns the distance between two vectors
        """
        if len(vector_one) != len(vector_two):
            raise ValueError("Point dimension mismatch")

        diff = np.subtract(vector_one, vector_two)

        return VectorMath.get_vector_magnitude(diff)

    @staticmethod
    def get_unit_vector_from_two_vectors(vector_one, vector_two):
        """
        Returns the unit vector of two vectors
        """
        unit_vector = np.subtract(vector_two, vector_one) / VectorMath.get_magnitude(vector_one, vector_two)

        return unit_vector

    @staticmethod
    def get_single_unit_vector(vector):
        """
        Returns the unit vector of a vector
        """
        unit_vector = vector / VectorMath.get_vector_magnitude(vector)

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
        mag = VectorMath.get_vector_magnitude(vector_two)

        return vector_two * (dot_prod / (mag**2))

    @staticmethod
    def get_vector_rejection(vector_one, vector_two):
        """
        Returns the vector rejection between two vectors
        """
        projection_vector = VectorMath.get_vector_projection(vector_one, vector_two)

        return np.subtract(vector_one, projection_vector)
    
    @staticmethod
    def get_force(vector_one, vector_two):
        """
        Return the force vector between two points
        """
        distance_vector = np.subtract(vector_one, vector_two)

        if distance_vector[2]:
            force_vector = np.array([1000.0/pow(distance_vector[0],2),1000.0/pow(distance_vector[1],2),1000.0/pow(distance_vector[2],2)])
        else:
            force_vector = np.array([1000.0/pow(distance_vector[0],2),1000.0/pow(distance_vector[1],2), 0])
        return force_vector

    @staticmethod
    def get_attractive_force(vector_one, vector_two):
        """
        Return the force vector between two points
        """
        distance_vector = np.subtract(vector_one, vector_two)

        if distance_vector[2]:
            force_vector = np.array([10000000.0/pow(distance_vector[0],2),10000000.0/pow(distance_vector[1],2),10000000.0/pow(distance_vector[2],2)])
        else:
            force_vector = np.array([10000000.0/pow(distance_vector[0],2),10000000.0/pow(distance_vector[1],2), 0])
        return force_vector

    # @staticmethod
    # def get_attractive_force(vector_one, vector_two):
    #     """
    #     Return the attractive force vector between waypoints and drone
    #     """
    #     distance_vector = np.subtract(vector_one, vector_two)
    #     force_vector = np.array([10.0/pow(distance_vector[0],2),10.0/pow(distance_vector[1],2),10.0/pow(distance_vector[2],2)])
    #     return force_vector