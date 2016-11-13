'''
Created on Nov 5, 2016

@author: phusisian
'''

import string
import LetterFrame

class LetterFrames:
    
    
    
    def __init__(self, fontIn, sizeIn):
        self.font = fontIn
        self.size = sizeIn
        self.letterFrames = []
        self.setLetterFrames()
    
    
    
    def getBestFitLetterFrameFromLeastSquare(self, lines):
        lowestIndex = 0
        lowestNum = self.letterFrames[0].getLeastSlopeSquare(lines)
        for i in range(1, len(self.letterFrames)):
            if self.letterFrames[i].getLeastSlopeSquare(lines) > lowestNum:
                lowestNum = self.letterFrames[i].getLeastSlopeSquare(lines)
                lowestIndex = i
        
        return self.letterFrames[lowestIndex]
    
    
    def getBestFitLetterFrame(self, imgIn):  #ISSUE: J is cropped by i and l because they are think letters. There are no parts of J's frame inside of i or l because of this, so numMissed is zero. SOLVE IN THE FUTURE BY MOVING THE WIREFRAME TO FIT THE IMAGE (moving all the points in it)
        fitIndex = 0
        #firstFound = False
        for i in range(0, len(self.letterFrames)):
            #print(self.letterFrames[i].compareImagesUsingOverlay(imgIn))
            if self.letterFrames[i].compareImagesUsingOverlay(imgIn) < self.letterFrames[fitIndex].compareImagesUsingOverlay(imgIn):
                fitIndex = i
            elif self.letterFrames[i].compareImagesUsingOverlay(imgIn) == self.letterFrames[fitIndex].compareImagesUsingOverlay(imgIn) and self.letterFrames[i].getNumFramePixels() > self.letterFrames[fitIndex].getNumFramePixels():
                #print(str(self.letterFrames[i].compareImagesUsingOverlay(imgIn)) + " %")
                fitIndex = i
                
                #if firstFound == True and self.letterFrames[i].getNumFramePixels() > self.letterFrames[fitIndex].getNumFramePixels():
                    #fitIndex = i
        return self.letterFrames[fitIndex]
        '''
        bestFitIndex = [0]
        bestFitNum = self.letterFrames[0].compareImagesUsingOverlay(imgIn)
        for i in range(0, len(self.letterFrames)):
            if self.letterFrames[i].compareImagesUsingOverlay(imgIn) < bestFitNum:
                bestFitNum = self.letterFrames[i].compareImagesUsingOverlay(imgIn)
                #bestFitIndex = i
                bestFitIndex = []
                bestFitIndex.append(i)
            elif bestFitNum != self.letterFrames[0].compareImagesUsingOverlay(imgIn) and self.letterFrames[i].compareImagesUsingOverlay(imgIn) == bestFitNum:
                bestFitIndex.append(i)
        if len(bestFitIndex) == 1:
            return self.letterFrames[bestFitIndex[0]]
        else:
            #print("TIE")
            #print(len(bestFitIndex))
            biggestAreaIndex = 0
            for i in range(0, len(bestFitIndex)):
                print(self.letterFrames[bestFitIndex[i]].getNumFramePixels() > self.letterFrames[bestFitIndex[biggestAreaIndex]].getNumFramePixels())
                if self.letterFrames[bestFitIndex[i]].getNumFramePixels() > self.letterFrames[bestFitIndex[biggestAreaIndex]].getNumFramePixels():
                    biggestAreaIndex = i
            return self.letterFrames[bestFitIndex[biggestAreaIndex]]
        #imgIn.show()
        
        #return self.letterFrames[bestFitIndex[0]]'''
    
    def setLetterFrames(self):
        '''
        letter = dict(enumerate(string.ascii_lowercase, 1))
        
        for i in range(1, 26):
            self.letterFrames.append(LetterFrame.LetterFrame(letter[i], self.font, self.size))
            '''
        letter = dict(enumerate(string.ascii_uppercase, 1))
        
        for i in range(1, 26):
            self.letterFrames.append(LetterFrame.LetterFrame(letter[i], self.font, self.size))
    
    def showAllFrames(self):
        for i in range(0, len(self.letterFrames)):
            self.letterFrames[i].show()
            
    def checkAccuracy(self):
        letter = dict(enumerate(string.ascii_lowercase, 1))
        #for i in range(1, 26):
        for i in range(1, 26):
            lf = LetterFrame.LetterFrame(letter[i], self.font, self.size)
            if self.getBestFitLetterFrame(lf.getImage()).getLetter() != lf.getLetter():
                #print(lf.getLetter())
                print(lf.getLetter())
                print("WRONG: " + self.getBestFitLetterFrame(lf.getImage()).getLetter())
                #lf.compareImagesUsingOverlayOutput(self.getBestFitLetterFrame(lf.getImage()).getImage()).show()
            else:
                #print(lf.getLetter())
                print("RIGHT")
                
                #lf.compareImagesUsingOverlayOutput(getBestFitLetterFrame(lf.getImage()))).show()
                #self.getBestFitLetterFrame(lf.getImage()).compareImagesUsingOverlayOutput(lf.getImage()).show()
            #if lf.compareImagesUsingOverlay(self.letterFrames[i].getImage()) != 0:
                #print("WRONG")
                
        letter = dict(enumerate(string.ascii_uppercase, 1))
        #for i in range(1, 26):
        for i in range(1+(len(self.letterFrames)/2), len(self.letterFrames)):
            lf = LetterFrame.LetterFrame(letter[i-25], self.font, self.size)
            if self.getBestFitLetterFrame(lf.getImage()).getLetter() != lf.getLetter():
                print(lf.getLetter())
                print("WRONG")
            else:
                #print(lf.getLetter())
                print("RIGHT")
            #if lf.compareImagesUsingOverlay(self.letterFrames[i].getImage()) != 0:
                #print("WRONG")
                