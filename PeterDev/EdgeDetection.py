'''
Created on Nov 3, 2016

@author: phusisian
'''
from PIL import Image
import Point
from SystemEvents.Standard_Suite import color

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
    
    def getLetterEdges(self, imgIn):
        image = imgIn.load()
        dim = imgIn.size
        edges = [[False for i in range(dim[1])] for j in range(dim[0])]
        for y in range(1, dim[1]):
            for x in range(1, dim[0]):
                if image[x, y] != image[x-1,y]:
                    edges[x][y] = True
                #if image[x-1,y-1] != image[x,y] or image[x-1,y] != image[x,y] or image[x,y-1] != image[x,y]:
                    #edges[x][y] = True
        return edges
    
    def drawEdges(self, edges, color):
        img = Image.new("RGB",[len(edges), len(edges[0])])
        print(len(edges))
        if len(edges) == img.size[0]:
            print("width same")
        else:
            print("edge width: {}".format(len(edges)))
            print("image width: {}".format(img.size[0]))
            print("edge height: {}".format(len(edges[0])))
            print("image height: {}".format(img.size[1]))
        if len(edges[0]) == img.size[1]:
            print("height same")
        else:
            print("edge height: {}".format(len(edges[0])))
            print("image height: {}".format(img.size[1]))
        image = img.load()
        dim = img.size
        for x in range(0, dim[0]):
            for y in range(0, dim[1]):
                #print("x: {}".format(x))
                #print("Y: {}".format(y))
                #try:
                if edges[x][y] == True:
                    #print(x)
                    #print(y)
                    image[x,y] = color
                #break
                #except
                    
        return img
    
    def drawEdgesOntoImage(self, img, edges, color):
        #img = Image.new("RGB",[len(edges), len(edges[0])])
        print(len(edges))
        if len(edges) == img.size[0]:
            print("width same")
        else:
            print("edge width: {}".format(len(edges)))
            print("image width: {}".format(img.size[0]))
            print("edge height: {}".format(len(edges[0])))
            print("image height: {}".format(img.size[1]))
        if len(edges[0]) == img.size[1]:
            print("height same")
        else:
            print("edge height: {}".format(len(edges[0])))
            print("image height: {}".format(img.size[1]))
        image = img.load()
        dim = img.size
        for x in range(0, dim[0]):
            for y in range(0, dim[1]):
                if x < len(edges) and y < len(edges[0]):
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
            
        