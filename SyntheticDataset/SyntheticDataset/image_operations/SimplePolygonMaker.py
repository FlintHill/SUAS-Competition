from math import pi
from math import sin
from math import cos
from SyntheticDataset.image_operations import *

class SimplePolygonMaker(object):
    '''No support for star, cross, or trapezoid currently'''
    numPointsCircle = 64
    thetaAddCircle = 2.0*pi/float(numPointsCircle)

    @staticmethod
    def createPolygonPointsInt(midpoint, radius, numPoints, rotation):#where rotation is the angle from the first point to the positive x axis
        points = SimplePolygonMaker.createPolygonPoints(midpoint, radius, numPoints, rotation)
        for point in points:
            point.setX(int(point.getX()))
            point.setY(int(point.getY()))
        return points

    @staticmethod
    def createPolygonPoints(midpoint, radius, numPoints, rotation):#where rotation is the angle from the first point to the positive x axis
        points = []
        thetaAdd = float(2*pi/float(numPoints))
        theta = rotation - pi/2.0#for some reason pi/2.0 is subtracted for it to function properly...
        numPoint = 0
        while numPoint < numPoints:
            x = midpoint.getX() + radius*cos(theta)
            y = midpoint.getY() + radius*sin(theta)
            appendPoint = Point(x,y)
            points.append(appendPoint)
            theta += thetaAdd
            numPoint += 1
        return points

    @staticmethod
    def createPolygonPointsUsingThetaBoundsInt(midpoint, radius, numPoints, startRotation, endRotation):
        points = []
        thetaAdd = float((endRotation-startRotation)/float(numPoints))
        numPoint = 0
        theta = startRotation
        while numPoint <= numPoints:
            x = int(midpoint.getX() + radius*cos(theta))
            y = int(midpoint.getY() + radius*sin(theta))
            appendPoint = Point(x,y)
            points.append(appendPoint)
            theta += thetaAdd
            numPoint += 1
        points.append(midpoint)
        return points

    @staticmethod
    def createSquareInt(midpoint, radius, rotation):
        rotationOffset = pi/4.0
        return Polygon(SimplePolygonMaker.createPolygonPointsInt(midpoint, radius, 4, rotation + rotationOffset))

    @staticmethod
    def createTriangleInt(midpoint, radius, rotation):
        return Polygon(SimplePolygonMaker.createPolygonPointsInt(midpoint, radius, 3, rotation))

    @staticmethod
    def createRectangleInt(midpoint, width, height, rotation):
        points = []
        points.append(Point(midpoint.getX() - width/2, midpoint.getY() - height/2))
        points.append(Point(midpoint.getX() + width/2, midpoint.getY() - height/2))
        points.append(Point(midpoint.getX() + width/2, midpoint.getY() + height/2))
        points.append(Point(midpoint.getX() - width/2, midpoint.getY() + height/2))
        for i in range(0, len(points)):
            points[i].rotate(midpoint, rotation)
            points[i] = points[i].toInt()
        return Polygon(points)

    @staticmethod
    def createSemicircleInt(midpoint, radius, rotation):
        rotationOffset = pi/2.0
        semiCirclePoints = SimplePolygonMaker.createPolygonPointsUsingThetaBoundsInt(midpoint, radius, SimplePolygonMaker.numPointsCircle/2, rotationOffset + rotation, rotationOffset + rotation + pi)
        return Polygon(semiCirclePoints)
        '''circle = SimplePolygonMaker.createCircleInt(midpoint, radius)

        cropRect = Rectangle(midpoint.getX() -radius, midpoint.getY() - radius, 2*radius, radius)
        circle.crop(cropRect)
        circle.rotate(midpoint, rotation)
        circle.toInt()
        return Polygon(circle.getPoints())'''


    @staticmethod
    def createQuartercircleInt(midpoint, radius, rotation):
        rotationOffset = pi/2.0
        quarterCirclePoints = SimplePolygonMaker.createPolygonPointsUsingThetaBoundsInt(midpoint, radius, SimplePolygonMaker.numPointsCircle/4, rotationOffset + rotation, rotationOffset + rotation + (pi/2.0))
        return Polygon(quarterCirclePoints)
        '''circle = SimplePolygonMaker.createCircleInt(midpoint, radius)
        #circle = Polygon(circlePoints)
        cropRect = Rectangle(midpoint.getX()-radius, midpoint.getY() - radius, radius, radius)
        circle.crop(cropRect)
        circle.insert(0, midpoint)
        #NO ROTATION IS APPLIED
        circlePoly = Polygon(circle.getPoints())
        circlePoly.rotate(midpoint, rotation)
        circlePoly.toInt()
        return circlePoly'''

    @staticmethod
    def createPentagonInt(midpoint, radius, rotation):
        return Polygon(SimplePolygonMaker.createPolygonPointsInt(midpoint, radius, 5,  rotation))

    @staticmethod
    def createHexagonInt(midpoint, radius, rotation):
        return Polygon(SimplePolygonMaker.createPolygonPointsInt(midpoint, radius, 6, rotation))

    @staticmethod
    def createHeptagonInt(midpoint, radius, rotation):
        return Polygon(SimplePolygonMaker.createPolygonPointsInt(midpoint, radius, 7, rotation))

    @staticmethod
    def createOctagonInt(midpoint, radius, rotation):
        initOffset = 0.125*pi
        return Polygon(SimplePolygonMaker.createPolygonPointsInt(midpoint, radius, 8, rotation + initOffset))

    @staticmethod
    def createCircleInt(midpoint, radius):
        return Polygon(SimplePolygonMaker.createPolygonPointsInt(midpoint, radius, SimplePolygonMaker.numPointsCircle, 0))
