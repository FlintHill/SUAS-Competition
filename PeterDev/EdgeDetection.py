'''
Created on Nov 3, 2016

@author: phusisian
'''
from PIL import Image
import Point

class EdgeDetection:
    def getKMeansEdges(self, imgIn):
        image = imgIn.load()
        dim = imgIn.size
        edges = [[False for i in range(dim[1])] for j in range(dim[0])]
        for x in range(1, dim[0]):
            for y in range(1, dim[1]):
                if image[x-1,y-1] != image[x,y] or image[x-1,y] != image[x,y] or image[x,y-1] != image[x,y]:
                    edges[x][y] = True
        return edges
    
    def drawEdges(self, edges, color):
        img = Image.new("RGB",[len(edges[0]), len(edges[1])])
        image = img.load()
        dim = img.size
        for x in range(0, dim[0]):
            for y in range(0, dim[1]):
                if edges[x][y] == True:
                    image[x,y] = color
                    
        return img
    
    def getEdgesAtRow(self, edges, row):
        points = []
        numSwitched = 0
        for x in range(1, len(edges)):
            if edges[x][row] != edges[x-1][row]:
                numSwitched += 1
                if numSwitched % 2 == 0:
                    p = Point.Point(x, row)
                    points.append(p)
        return points
    
    def getEdgesAtColumn(self, edges, column):
        points = []
        numSwitched = 0
        for y in range(1, len(edges[0])):
            if edges[column][y] != edges[column][y-1]:
                numSwitched += 1
                if numSwitched %2 == 0:
                    p = Point.Point(column, y)
                    points.append(p)
        return points
            
        