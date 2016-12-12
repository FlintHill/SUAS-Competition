from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from root.nested.SobelEdge import SobelEdge
from root.nested.ColorSeparation import ColorSeparation
from root.nested.ColorLayers import ColorLayers
from root.nested.ColorLayer import ColorLayer
from root.nested.AngleFitter import AngleFitter
from root.nested.GaussianBlur import GaussianBlur

class LetterFrame:
    
    '''***Idea: for user understandability and simplicity, consider making a new image made up of ONLY angles, layer by layer, so, say, F, would turn into 
    
    ____         instead of _____
    |___                    |  (with variable gap here)
    |                       |____
                            |
                            |  (with variable gap here)
    '''
    
    '''***Remember that there could be flawed comparisons between letters that have a "tail" 
    that goes under the line (q for example). Tailed letter will be compared at the same height
     as normal, as if the tail were on the line***'''
    
    def __init__(self, letterIn, fontIn, sizeIn):
        self.font = ImageFont.truetype(fontIn, sizeIn)
        self.size = sizeIn
        self.letter = letterIn
        self.setLetterImg()
        
        cropLayer = ColorLayer(self.letterImg, self.letterImage, (255,255,255))
        cropLayer.cropLayerToBounds()
        self.letterImg = cropLayer.getColorImg()
        self.letterImage = cropLayer.getColorImage()#may not be necessary to update letterImage, might update on crop
        self.sobelEdge = SobelEdge(self.letterImg, self.letterImage)
        self.angleFitter = AngleFitter(self.sobelEdge)
      
    
    '''def resizeLetterFrame(self, sizeRect):
        self.letterImg = self.letterImg.resize(sizeRect.getWidth(), sizeRect.getHeight())
        self.letterImage = self.letterImg.load()
        self.sobelEdge = SobelEdge(self.letterImg, self.letterImage)
        self.angleFitter = AngleFitter(self.sobelEdge)
        
          '''
        
    def getDim(self):
        return self.letterImg.size    
        
    def getLeastSquareFit(self, sobelEdgeIn, threshold):
        return self.angleFitter.getLeastSquareFit(sobelEdgeIn, threshold)    
       
    def getSobelEdge(self):
        return self.sobelEdge  
    
    #def cropAndResize(self):
        
      
    def getAngleImage(self):
        return self.sobelEdge.getAngleImage(0)
    
    def showLetterImg(self):
        self.letterImg.show()
        
    def getLetter(self):
        return self.letter
    
    def setLetterImg(self):
        self.letterImg = Image.new("RGB", (self.size*3,self.size*3))
        draw = ImageDraw.Draw(self.letterImg)
        draw.fontmode = "1" #one sets to not antialias. If camera antialiases, set to zero.
        draw.text((1,1), self.letter, (255,255,255), font = self.font)
        self.letterImage = self.letterImg.load()
        self.letterImg = GaussianBlur.getGaussianFilteredImage(self.letterImg, self.letterImage, 3)
    
        