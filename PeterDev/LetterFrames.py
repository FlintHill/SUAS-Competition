import string
from root.nested.LetterFrame import LetterFrame

class LetterFrames:
    
    frameHeight = 0
    def __init__(self, font, size):
        self.font = font
        self.size = size
        self.initLetterFrames()
        LetterFrames.frameHeight = self.letterFrames[0].getDim()[1]#could switch to using average height
        print("Frame Height: " + str(LetterFrames.frameHeight))
        #frameHeight = self.letterFrames[0].getDim()[1]#could switch to using average height
    
        
    #could solve I fit problem (horizontal lines vs. no horizontal lines) by generating two sets of I's (one with, one without) in my letter frames    
    def initLetterFrames(self):
        self.letterFrames = []
        letterList = dict(enumerate(string.ascii_uppercase, 0))
        
        for i in range(0, len(letterList)):
            print(letterList[i])
            self.letterFrames.append(LetterFrame(letterList[i], self.font, self.size))
    
    def __getitem__(self, index):
        return self.letterFrames[index] 
    
    def __len__(self):
        return len(self.letterFrames)       
    
    def getLetterFrames(self):
        return self.letterFrames
    
    '''def getAverageFrameHeight(self):
        heightAdd = 0
        for i in range(0, len(self)):
            heightAdd += self[i].getLetterImg().size[1]
        return float(heightAdd)/float(len(self))'''
    
    def getFrameHeight(self):
        return self[0].getLetterImg().size[1]
    
    def checkAccuracyUsingLeastSquare(self, compareLetterFrames, threshold):
        numCorrect = len(compareLetterFrames.getLetterFrames())
       
        for i in range(0, len(compareLetterFrames.getLetterFrames())):
            
            fitLetterFrame = self.getBestFitLetterFrameFromLetterFrame(compareLetterFrames.getLetterFrames()[i], threshold)
            
            if fitLetterFrame.getLetter() != compareLetterFrames.getLetterFrames()[i].getLetter():
                print("Fit Letter: " + fitLetterFrame.getLetter() + " Check Letter: " + str(compareLetterFrames.getLetterFrames()[i].getLetter()))
                numCorrect -= 1
               
        return float(numCorrect)/float(len(compareLetterFrames.getLetterFrames())) * 100.0
     
    def getBestFitLetterFrameFromLetterFrame(self, letterFrame, threshold):
        return self.getBestFitLetterFrameFromSobel(letterFrame.getSobelEdge(), threshold) 
       
    def getBestFitLetterFrameFromSobel(self, sobelEdge, threshold):
        leastSquareIndex = 0
        leastSquareNum = self.letterFrames[leastSquareIndex].getLeastSquareFit(sobelEdge, threshold)
        
        for i in range(1, len(self.letterFrames)):
            iterLeastSquare = self.letterFrames[i].getLeastSquareFit(sobelEdge, threshold)
            if iterLeastSquare < leastSquareNum:
                leastSquareNum = iterLeastSquare
                leastSquareIndex = i
        return self.letterFrames[leastSquareIndex]