'''
Created on Feb 7, 2017

@author: phusisian
'''
from root.nested.Vector import Vector
class PictureMatrix:
    
    def __init__(self, cannyImg, cannyImage):
        self.cannyImg = cannyImg
        self.cannyImage = cannyImage
        self.midpoint = (cannyImg.size[0]/2, cannyImg.size[1]/2)
        self.initMatrix()
        
        
    def initMatrix(self):
        self.means = [0 for i in range(0, 2)]
        self.matrix = []
        for x in range(0, self.cannyImg.size[0]):
            for y in range(0, self.cannyImg.size[1]):
                if self.cannyImage[x,y] != (0,0,0):
                    addVector = Vector([x - self.midpoint[0],y - self.midpoint[1]])
                    self.means[0] += addVector[0]
                    self.means[1] += addVector[1]
                    self.matrix.append(addVector)
        self.means[0] /= float(len(self.matrix))
        self.means[1] /= float(len(self.matrix))
        
    def getMeans(self):
        return self.means
    
    def getDim(self):
        return 2
    
    def __getitem__(self, index):
        return self.matrix[index]
    
    def __len__(self):
        return len(self.matrix)