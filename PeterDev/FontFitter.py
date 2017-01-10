'''
Created on Jan 10, 2017

@author: phusisian
'''
from root.nested.LetterFrame import LetterFrame
class FontFitter:
    
    def __init__(self, font, fontRange):
        self.fontRange = fontRange
        self.font = font
        self.initSizes()
        
    def initSizes(self):
        self.fontSizes = []
        for i in range(self.fontRange[0], self.fontRange[1]):
            sizeFrame = LetterFrame("A", self.font, i)
            self.fontSizes.append((i, sizeFrame.getLetterImg().size[1]))
            
    '''may have trouble finding a font to fit a size that ISN'T supported by any of the fonts added, may skip over it.
    Will have to find a way to instead get the best FITTING font'''
    def getBestFittingFontForSize(self, height):
        for i in range(0, len(self.fontSizes)):
            if self.fontSizes[i][1] == height:
                return self.fontSizes[i][0]
        return None