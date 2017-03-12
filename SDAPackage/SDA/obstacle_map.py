import numpy as np
from SDA import Drone
from SDA import StationaryObstacle
from SDA import VectorMath

class ObstacleMap(object):
    """
    Wrapper class for an obstacle map
    """

    def __init__(self):
        self.obstacles = np.array([[]])
        self.drone = Drone(np.array([0,0]))

    def add_obstacle(self, obstacle_to_add):
        """
        Add an obstacle to the map

        :param obstacle_to_add: The obstacle to add to the map
        :type obstacle_to_add: StationaryObstacle
        """
        pass

    def update_obstacles(self):
        """
        Update the obstacles' positions within the map (should be called
        when map is refreshed)
        """
        pass

    def is_obstacle_in_path(self):
        """
        Return True if drone should avoid obstacle and False if not
        """
        pass

    def get_avoid_coords(self):
        """
        Return the coordinates of a guided waypoint if obstacle is in path,
        else return None
        """
        pass
