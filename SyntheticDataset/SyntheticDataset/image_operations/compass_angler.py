import math
import random

class CompassAngler(object):
    COMPASS_ANGLES = [("E", 0), ("NE", math.pi/4.0), ("N", math.pi/2.0), ("NW", 3.0*math.pi/4.0), ("W", math.pi), ("SW", 5.0*math.pi/4.0), ("S", 3.0*math.pi/2.0), ("SE", 7.0*math.pi/4.0), ("E", 2.0*math.pi)]

    @staticmethod
    def getClosestCompassAngle(angle):
        sorted_angles = CompassAngler.getCompassAnglesSortedByProximityToAngle(angle)
        return sorted_angles[0][0]

    @staticmethod
    def getCompassAnglesSortedByProximityToAngle(angle ):
        unrotatedAngle = (angle + (math.pi/2.0))%(2.0*math.pi)
        if unrotatedAngle < 0:
            unrotatedAngle += 2.0*math.pi
        #print("angle in: " + str(angle))
        print("rounded angle: " + str(sorted(CompassAngler.COMPASS_ANGLES, key = lambda compass_angle : abs((unrotatedAngle - compass_angle[1]))%(2.0*math.pi))[0]))
        return sorted(CompassAngler.COMPASS_ANGLES, key = lambda compass_angle : abs((unrotatedAngle - compass_angle[1]))%(2.0*math.pi))

    @staticmethod
    def getRandomCompassAngle():
        randIndex = random.randint(0, len(CompassAngler.COMPASS_ANGLES) - 1)
        return CompassAngler.COMPASS_ANGLES[randIndex][1]
