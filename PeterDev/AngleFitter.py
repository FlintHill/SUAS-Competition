'''
Created on Dec 2, 2016

@author: phusisian
'''
import math
from root.nested.SobelEdge import SobelEdge
from PIL import Image

class AngleFitter:
    global widthThreshold
    widthThreshold = 2.5 #can be adjusted by back propegation
    
    def __init__(self, sobelEdge):
        self.sobelEdge = sobelEdge
        
        
    '''***Make sure that input letter is properly rotated so that the algorithm is accurate (least square are NOT off by a constant factor, which you might think since the letter would be skewed for all of them)
    Also, compareSobelStride is not enough for un-properly scaled inputs (e.g. comparing 50 point font to 100). compareSobelStride is used when the image needs to be flattened to better fit the other. Could make 
    an compareSobelXStride for how it iterates across if I want, but it's probably more user-friendly to scale the image to fit width-wise anyway, then flatten with compareSobelStride.***'''
    
    def getLeastSquareFitUsingResizedSobel(self, compareSobelEdge, threshold):
        squareNum = 0
        
        
        compareSobelYStride = 1#float(compareSobelEdge.getSobelEdgeImg().size[1])/float(self.sobelEdge.getSobelEdgeImg().size[1])#be wary of skipping over angles. This should really only be used to adjust small differences in height so the effect OUGHT to be negligible**
        #scaleX = float(self.sobelEdge.getImg().size[0])/float(compareSobelEdge.getImg().size[0])
        #scaleY = float(self.sobelEdge.getImg().size[1])/float(compareSobelEdge.getImg().size[1])
        
        resizedImg = compareSobelEdge.getImg().resize(self.sobelEdge.getImg().size)
        resizedImage = resizedImg.load()
        
        resizedCompareSobelEdge = SobelEdge(resizedImg, resizedImage)
        return self.getLeastSquareFit(resizedCompareSobelEdge, threshold)
        #***weird solution to keep in mind for the O Q swap problem: flip the image and and fit it to O, then fit it to Q, if it is Q, Q SHOULD score worse than it did before it was flipped. Otherwise, Q should score similarly***#
        '''
        #Reminder to resize input to fit other input so to fix O being Q
        
        for y in range(0, len(self.sobelEdge.getAngles()[0])):
            thisAnglesAtIndex = self.sobelEdge.getAnglesAtRow(y, threshold)
            compareAnglesAtIndex = resizedCompareSobelEdge.getAnglesAtRow(int(round(y * compareSobelYStride)), threshold)
            sortedCompareAngles = self.sortCompareAnglesByMinimumDifference(thisAnglesAtIndex, compareAnglesAtIndex)
            
            for i in range(0, len(sortedCompareAngles)):
                squareNum += (sortedCompareAngles[i] - thisAnglesAtIndex[i])**2
            
        return squareNum
        '''
    
    
    def getLeastSquareFit(self, compareSobelEdge, threshold):
        squareNum = 0
        
        
        compareSobelYStride = float(compareSobelEdge.getSobelEdgeImg().size[1])/float(self.sobelEdge.getSobelEdgeImg().size[1])#be wary of skipping over angles. This should really only be used to adjust small differences in height so the effect OUGHT to be negligible**
        
        
       
        #Reminder to resize input to fit other input so to fix O being Q
        if self.sobelEdgesWithinWidthThreshold(compareSobelEdge):
            for y in range(0, len(self.sobelEdge.getAngles()[0])):
                thisAnglesAtIndex = self.sobelEdge.getAnglesAtRow(y, threshold) #issue with getting angles at a row is that there could be an F with the second horizontal line moved slightly farther down. Would be best if I could get all relevant angles based on their height in a layer, e.g. these are the first lines from the top, these are the second, etc.
                #what may be best is to store angles by X and by Y, then iterate over the next relevant angle in each, match that way?
                compareAnglesAtIndex = compareSobelEdge.getAnglesAtRow(int(round(y * compareSobelYStride)), threshold)
                sortedCompareAngles = self.sortCompareAnglesByMinimumDifference(thisAnglesAtIndex, compareAnglesAtIndex)
                
                for i in range(0, len(sortedCompareAngles)):
                    squareNum += (sortedCompareAngles[i] - thisAnglesAtIndex[i])**2
            
            return squareNum
        '''very high number so that it can't possibly be the best fit. It technically is possible this could be the lowest, 
        depending how big the inputs are, so keep this in mind for error-finding (not likely to occur). See "Fluent Python" 
        for special method __bool__ (I think it's called) so that I could return -1 and it will not be counted in least square 
        at all)'''
        return 10000000
       
    def sobelEdgesWithinWidthThreshold(self, compareSobel):
        
        ratio = float(self.sobelEdge.getImg().size[0])/float(compareSobel.getImg().size[0])
        if (ratio < widthThreshold and ratio > 1.0/widthThreshold) or (1.0/ratio < widthThreshold and 1.0/ratio > 1.0/widthThreshold):
            return True
        return False
    
    '''***MAJOR: rows with different number of angles to compare get inaccurate
    readings from the angle optimization. For example, when compared with comic sans,
    most letters returned L as their fit since the majority of letters have a vertical 
    line somewhere. Angle optimization optimized the vertical angles to match the vertical 
    angles, giving a very low least square
     
    MAJOR: sorting for optimum fit can lead to inaccuracy, since each solid's start will have
    an edge that defines its second edge with an angle 180 degrees off from the first. This 
    leads to letters like A being confused with V since their angles are getting snapped to 
    their opposite edges and getting very low differences as a result***'''
    def sortCompareAnglesByMinimumDifference(self, thisAngles, compareAngles):#not sure if this actually optimizes or just slaps a decent guess (by cycling through and picking closest fit, maybe there is a way to rearrange so that difference is further optimized?)
        sortedAngles = []
        for i in range(0, len(thisAngles)):
            smallestDiffIndex = 0
            if len(compareAngles) > 0:
                smallestDiff = abs(self.getAngleDifference(compareAngles[smallestDiffIndex], thisAngles[i]))
                for j in range(1, len(compareAngles)):
                    angleDiff = abs(self.getAngleDifference(compareAngles[j], thisAngles[i]))
                    if angleDiff < smallestDiff:
                        smallestDiff = angleDiff
                        smallestDiffIndex = j
                sortedAngles.append(compareAngles[smallestDiffIndex])
                compareAngles.pop(smallestDiffIndex)
            else:
                sortedAngleLen = len(sortedAngles)
                for j in range(sortedAngleLen, len(thisAngles)):
                    sortedAngles.append(0)
                    thisAngles[i] = 2*math.pi#***This value can be tuned using back propegation, although keeping it at current value seems best for now. Maybe I could even threshold it on a per letter basis? E.g. most easily confused letters need more tuning? Playing around with value makes certain letters dissapear as false posistives and others appear.***#
                return sortedAngles
            
        for i in range(0, len(compareAngles)):
            sortedAngles.append(math.pi) #***This value can be tuned using back propegation, although keeping it current value seems best for now. Maybe I could even threshold it on a per letter basis? E.g. most easily confused letters need more tuning? Playing around with value makes certain letters dissapear as false posistives and others appear.***#
            thisAngles.append(0)
        return sortedAngles    
            
    
    '''Other possible idea: use traditional least square curve fit not as a function,
     but based on two cannys and points nearest to each other on a given column'''

    def getAngleDifference(self, a2, a1):
        return a1-a2