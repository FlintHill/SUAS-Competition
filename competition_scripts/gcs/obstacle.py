from math import sin, cos
from ObjAvoid import MultiDimPoint
class Obstacle:
    """
    Wrapper class for obstacles
    """
    STATIONARY_CONSTANT = 1.5
    def __init__(self, dist, heading, alt, radius, obstacle_type):
        """
        Initialize

        :param dist: The haversine distance from the origin to the obstacle
        :param heading: The heading calculated from the origin to the obstacle
        :param alt: The altitude of the obstacle
        :param radius: The radius of the obstacle
        :param obstacle_type: The type of the obstacle (either stationary or
            moving)
        """
        self.dist = dist
        self.heading = heading
        self.alt = alt
        self.radius = radius
        self.type = obstacle_type
        self.init_point()

    def init_point(self):
        dx = self.dist * cos(heading)
        dy = self.dist * sin(heading)
        self.point = MultiDimPoint([dx,dy,self.alt])
        
    
    def get_distance(self):
        """
        Return the distance
        """
        return self.dist

    def get_heading(self):
        """
        Return the heading
        """
        return self.heading

    def get_altitude(self):
        """
        Return the altitude
        """
        return self.alt

    def get_radius(self):
        """
        Return the radius
        """
        return self.radius

    def get_obstacle_type(self):
        """
        Return the obstacle's type
        """
        return self.type
    
    def get_point(self):
        '''
        Returns the XYZ Point of the obstacle's location relative to the origin
        '''
        return self.point
    
    def to_safety_radius_mass(self):
        if self.type == "stationary":
            
        else:
            
    def getSafetyRadius(self):
        '''returns safety radius calculated based on the radius of the obstacle as wel as whether
        it is moving or not'''
        if self.type == "stationary":
            return self.radius * obstacle.SAFETY_RADIUS
        else:
            '''this is temporary until we get a better calculation for 
            getting a safety radius for a moving obstacle'''
            movingConstant = 2
            return self.radius * movingConstant
            
    
    
