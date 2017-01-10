'''
Created on Jan 8, 2017

@author: phusisian
'''
class Circle:
    
    def __init__(self, xy, radius):
        self.xy = xy
        self.radius = radius
    
    def __getitem__(self, index):
        return self.xy[index]
    
    def getRadius(self):
        return self.radius