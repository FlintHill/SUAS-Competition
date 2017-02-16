from math import sqrt, atan2, pi
from numpy import angle



class Vector:
    
    def __init__(self, components):
        self.components = components
        
    def __getitem__(self, index):
        return self.components[index]
    
    def __len__(self):
        return len(self.components)
    
    def __add__(self, vectorTwo):
        resultVector = []
        try:
            for i in range(0, len(self)):
                resultVector.append(self[i] + vectorTwo[i])
            return Vector(resultVector)
        except:
            raise ValueError("Vectors added do not have same dimensions")
            return None
    
    @classmethod
    def createEmptyVectorWithDim(cls, dimNum):
        coords = []
        for i in range(0, dimNum):
            coords.append(0)
        return Vector(coords)
    
    def getMagnitude(self):
        squareSum = 0
        for i in range(0, len(self)):
            squareSum += self[i]**2
        return sqrt(squareSum)
    
    def __repr__(self):
        outString = ""
        for i in range(0, len(self)):
            outString += str(self[i]) + ", "
            
        return outString
    
    def __imul__(self, num):
        for i in range(0, len(self)):
            self.components[i] *= num
        return self
    
    def __mul__(self, num):
        components = []
        for i in range(0, len(self)):
            components.append(float(self.components[i]*num))
        return Vector(components)
    
    def getUnitVector(self):
        magnitude = float(self.getMagnitude())#cast to float in case it thinks its an int and rounds to it
        return self * (1.0/magnitude)
      
    def getProjectionOntoSelf(self, vectorTwo):
        #print(vectorTwo)
        dotProd = self.dotProduct(vectorTwo)
        #print(dotProd)
        mag = self.getMagnitude()
        return self*(dotProd/(mag**2))
    
    def dotProduct(self, vectorTwo):
        try:
            sum = 0
            for i in range(0, len(vectorTwo)):  
                sum += self[i]*vectorTwo[i]
            return sum
        except:
            raise ValueError("Vectors added do not have same dimensions")
        
    def draw2D(self, img, image, center, color):
        unitVector = self.getUnitVector()
        magnitude = self.getMagnitude()
        for t in range(0, int(magnitude)):
            x = center[0] + int(unitVector[0] * t)
            y = center[1] - int(unitVector[1] * t)
            if x > 0 and x < img.size[0] and y > 0 and y < img.size[1]:
                image[x,y] = color
                
        return None
            
    
    def getTheta2D(self):
        angle = atan2(self.components[1], self.components[0])
        if angle < 0:
            angle += 2*pi
        return angle
    
    def __iadd(self, vectorTwo):
        try:
            for i in range(0, len(self)):
                self[i] += vectorTwo[i]
            return self
        except:
            raise ValueError("Vectors added do not have same dimensions")
    