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
        force_vector = np.array([])

        if distance_vector[2]:
            for distance in distance_vector:
                if distance != 0:
                    force = 100/distance
                    force_vector = np.hstack([force_vector, force])
                else:
                    force_vector = np.hstack([force_vector, 100000])
        else:
            for distance in distance_vector:
                if distance != 0:
                    force = 100/distance
                    force_vector = np.hstack([force_vector, force])
                else:
                    force_vector = np.hstack([force_vector, 100000])
        return force_vector

    @staticmethod
    def get_repulsive_force(obstacle, waypoint):
        distance_vector = np.subtract(waypoint, obstacle.point)
        distance_vector_magnitude = VectorMath.get_vector_magnitude(distance_vector)
        distance_vector_unit_vector = VectorMath.get_single_unit_vector(distance_vector)
        detection_magnitude = distance_vector_magnitude - obstacle.radius

        force_vector = np.array([])
        if distance_vector[2]:
            detection_vector = np.array([distance_vector_unit_vector[0]*detection_magnitude, distance_vector_unit_vector[1]*detection_magnitude])
            for distance in detection_vector:
                if distance != 0:
                    force = 100.0/distance
                    force_vector = np.hstack([force_vector, force])
                else: 
                    np.hstack([force_vector, 100000])
          
        else:
            detection_vector = np.array([distance_vector_unit_vector[0]*detection_magnitude, distance_vector_unit_vector[1]*detection_magnitude])
            for distance in detection_vector:
                if distance != 0:
                    print(distance)
                    force = 100.0/distance
                    force_vector = np.hstack([force_vector, force])
                else:
                    np.hstack([force_vector, 100000])
        # else:
           # old method
        #     detection_vector = np.array([distance_vector_unit_vector[0]*detection_magnitude, distance_vector_unit_vector[1]*detection_magnitude])
        #     force_vector = np.array([100.0/pow(detection_vector[0],1),100.0/pow(detection_vector,1), 0])
        #     print(force_vector)
        print(force_vector)
        return force_vector



    @staticmethod
    def get_attractive_force(vector_one, vector_two, obstacles):
        """
        Return the force vector between two points
        """
        distance_vector = np.subtract(vector_one, vector_two)
        force_multiplier = obstacles.size
        force_vector = np.array([])

        if distance_vector[2]:
            for distance in distance_vector:
                force = (100* force_multiplier)/distance
                force_vector = np.hstack([force_vector, force])
        else:
            for distance in distance_vector:
                force = (100*force_multiplier)/distance
                force_vector = np.hstack([force_vector, force])
        return force_vector

   