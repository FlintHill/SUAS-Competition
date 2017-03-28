from imageop.Point import Point
from math import sqrt

class Line:
    def __init__(self, p1In, p2In):
        self.p1 = p1In
        self.p2 = p2In
        self.setSlope()
    
    '''slope will change if either point is edited. If dx is zero, divide by zero occurs. Fixed by slightly slanting line.
    this is called by functions without mentioning it in their name (which would add needless baggage and only serves for
    the line to function properly after edits are made.'''
    def setSlope(self):
        dx = self.p2.getX() - self.p1.getX()
        if dx != 0:
            self.slope = float(self.p2.getY() - self.p1.getY())/(self.p2.getX() - self.p1.getX())
        else:
            self.slope = float(self.p2.getY() - self.p1.getY())/(0.001)
    
    '''treats the line as a function and returns the y value at a given x of the line.'''
    def getYAsFunction(self, xIn):
        return self.slope*xIn - self.slope*self.p1.getX() + self.p1.getY()
    
    '''returns the parametric value of x for a given t inputted'''
    def getXParametric(self, tIn):
        return self.p1.getX() + self.getDX()*tIn
    
    '''returns the parametric value of y for a given t inputted'''
    def getYParametric(self, tIn):
        return self.p1.getY() + self.getDY()*tIn
    
    '''returns delta x of the line'''
    def getDX(self):
        return self.p2.getX() - self.p1.getX()
    
    '''returns delta y of the line'''
    def getDY(self):
        return self.p2.getY() - self.p1.getY()
    
    '''draws the line'''
    def draw(self, image, color):
        magnitude = self.getMagnitude()
        tStep = 1.0
        if magnitude != 0:
            tStep /= magnitude
        t = 0
        while t < 1:
            #it's possible that it could skip a pixel because of rounding since tStep is a float
            xVal = int(round(self.getXParametric(t)))
            yVal = int(round(self.getYParametric(t)))
            image[xVal,yVal] = color
            t += tStep
            
    '''Draws a translated version of the line, based on a point whose x and y are dy, dx of the line
    would be better if this returned a different version of draw with a new line object so if I edit normal draw, this is edited as well.
    works for now, so am not changing for the moment.'''
    def drawTranslatedLine(self, image, color, translatePoint):
        magnitude = self.getMagnitude()
        tStep = 1.0
        if magnitude != 0:
            tStep /= magnitude
        t = 0
        while t < 1:
            #it's possible that it could skip a pixel because of rounding since tStep is a float
            xVal = int(round(self.getXParametric(t))) + translatePoint.getX()
            yVal = int(round(self.getYParametric(t))) + translatePoint.getY()
            #print("X Val: " + str(xVal) + " Y Val: " + str(yVal))
            image[xVal,yVal] = color
            t += tStep
        
    '''might want to implement python's special method for magnitude.'''
    def getMagnitude(self):
        return sqrt(self.getDX()**2 + self.getDY()**2)
    def getSlope(self):
        return self.slope
    def getP1(self):
        return self.p1
    def getP2(self):
        return self.p2
    '''returns "b" in the slope intercept formula, y = mx + b. '''
    def getB(self):
        return self.slope*self.p1.getX() + self.p1.getY()
    
    '''
    ---------------------------------------------------------------------------------------------------------
    The below are untested, as their original function was abandoned for a simpler method (polygon filling). 
    They may be useful in the future, so I've kept them here.
    
    Parametric intersection functions may or may not work. Keep in mind. Originally made for drawing polygons
    but drawing into blank images and masking them over using pixel scanning instead of math was used instead
    ---------------------------------------------------------------------------------------------------------'''
    
    def getParametricPoint(self, tIn):
        return Point(self.getXParametric(tIn), self.getYParametric(tIn))
    
    def getTAtY(self, compareY):
        dy = self.getDY()
        if dy != 0:
            return (compareY - self.p1.getY())/dy
        return 0
    
    def getIntersectionAtY(self, compareY):
        t = self.getTAtY(compareY)
        return self.getParametricPoint(t)
    
    def getBoundedIntersectionAtY(self, compareY):
        t = self.getTAtY(compareY)
        if t >= 0 and t <= 1:
            return self.getParametricPoint(t)
        return False
    
    #returns a point that is the intersection of the two lines. Obviously doesn't work if they are parallel, or the same line.
    def getIntersectionPoint(self, compareLine):
        intersectT = self.getParametricIntersectT(compareLine)
        return Point(self.getXParametric(intersectT), self.getYParametric(intersectT))
       
    def getBoundedIntersectionPoint(self, compareLine):
        intersectT = self.getParametricIntersectT(compareLine)
        if intersectT <= 1 and intersectT >= 0:
            return Point(self.getXParametric(intersectT), self.getYParametric(intersectT))
        return False
        
    def getParametricIntersectT(self, compareLine):
        #t = (ay2 - ay1 - bx2 + bx1)/(bc-ad)#where line 2 is this line.
        numerator = (compareLine.getDX()*self.p1.getY() - compareLine.getDX()*compareLine.getP1().getY() - compareLine.getDY()*self.p1.getX() + compareLine.getDY()*compareLine.getP1().getX())
        denominator = (compareLine.getDY()*self.getDX() - compareLine.getDX()*self.getDY())
        t = 0
        if denominator != 0:#so you don't divide by zero
            t = numerator/denominator
        return t
    