'''
Created on Jan 10, 2017

@author: phusisian
'''
from math import sqrt

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

    '''multiplies the vector by a constant'''#may be swaping mul and imul's fucntion
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
        magnitude = self.getMagnitude()
        return self * (1.0/float(magnitude))

    def getProjectionOntoSelf(self, vectorTwo):
        dotProd = self.dotProduct(vectorTwo)
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

    def __iadd(self, vectorTwo):
        try:
            for i in range(0, len(self)):
                self[i] += vectorTwo[i]
            return self
        except:
            raise ValueError("Vectors added do not have same dimensions")
