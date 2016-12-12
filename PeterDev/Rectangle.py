class Rectangle:
    def __init__(self, xIn, yIn, widthIn, heightIn):
        self.x = xIn
        self.y = yIn
        self.width = widthIn
        self.height = heightIn
       
    def __repr__(self):
        return "X: " + str(self.x) + " Y: " + str(self.y) + " Width: " + str(self.width) + " Height: " + str(self.height)
        
    def getHeight(self):
        return self.height
    def getWidth(self):
        return self.width
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def setX(self, xIn):
        self.x = xIn
    def setY(self, yIn):
        self.y = yIn
    
    def getMidpoint(self):
        return ((2*self.x+self.width)/2.0, (2*self.y+self.height)/2.0)    
    
    def setWidth(self, widthIn):
        self.width = widthIn
    def setHeight(self, heightIn):
        self.height = heightIn
        