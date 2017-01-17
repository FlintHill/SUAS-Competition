from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from root.nested.SobelEdge import SobelEdge
from root.nested.ColorSeparation import ColorSeparation
from root.nested.ColorLayers import ColorLayers
from root.nested.ColorLayer import ColorLayer
from root.nested.AngleFitter import AngleFitter
from root.nested.GaussianBlur import GaussianBlur
from root.nested.CannyEdge import CannyEdge
from root.nested.HarrisCorner import HarrisCorner
from root.nested.HoughCircles import HoughCircles
class LetterFrame:
    
    
    HARRIS_THRESHOLD = 750000
    HARRIS_KERNELSIZE = 3
    HARRIS_STDDEV = 5
    CIRCLE_THRESHOLD = 40
    '''This needs to be tuned based on the font size. However, performance doesn't seem too affected, 
    since it goes by a range of circles. It just happens that the circles it finds are smaller'''
    RADIUS_BOUNDS = (7, 19)
   
    
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
        #self.angleFitter = AngleFitter(self.sobelEdge)
        self.cannyImg = CannyEdge.getCannyEdgeImage(self.sobelEdge, 40, 20)
        self.corners = HarrisCorner.getCorners(self.letterImg, self.letterImage, self.sobelEdge, LetterFrame.HARRIS_KERNELSIZE, LetterFrame.HARRIS_STDDEV, LetterFrame.HARRIS_THRESHOLD)
        self.houghCircles = HoughCircles(self.cannyImg, self.cannyImg.load(), LetterFrame.RADIUS_BOUNDS)
        self.circles = self.houghCircles.getCirclesOverThreshold(LetterFrame.CIRCLE_THRESHOLD)
        #cannyImgCopy = self.cannyImg.copy()
        #self.houghCircles.circleCirclesOverThreshold(cannyImgCopy, cannyImgCopy.load(), LetterFrame.CIRCLE_THRESHOLD).show()
        #self.dimRatio = float(self.letterImg.size[0])/float(self.letterImg.size[1])
        #self.letterImg.show()
    
    '''def resizeLetterFrame(self, sizeRect):
        self.letterImg = self.letterImg.resize(sizeRect.getWidth(), sizeRect.getHeight())
        self.letterImage = self.letterImg.load()
        self.sobelEdge = SobelEdge(self.letterImg, self.letterImage)
        self.angleFitter = AngleFitter(self.sobelEdge)
        
          '''
    '''multiply the desired font by this ratio to get the correct font height for it'''
    @staticmethod
    def getHeightToFontRatio(fontIn):
        HundredPointA = LetterFrame("A", fontIn, 100)
        return 100.0/float(HundredPointA.getLetterImg().size[1])
      
    def getDimRatio(self):
        return self.dimRatio
    
    def getCircles(self):
        return self.circles
    
    def getDim(self):
        return self.letterImg.size    
        
    def getLeastSquareFit(self, sobelEdgeIn, threshold):
        return self.angleFitter.getLeastSquareFit(sobelEdgeIn, threshold)    
    
    def getCorners(self):
        return self.corners
       
    def getSobelEdge(self):
        return self.sobelEdge  
    
    def getCannyImg(self):
        return self.cannyImg
    
    #def cropAndResize(self):
        
      
    def getAngleImage(self):
        return self.sobelEdge.getAngleImage(0)
    
    def showLetterImg(self):
        self.letterImg.show()
        
    def getLetter(self):
        return self.letter
    
    def getLetterImg(self):
        return self.letterImg
    
    def setLetterImg(self):
        self.letterImg = Image.new("RGB", (self.size*3,self.size*3))
        draw = ImageDraw.Draw(self.letterImg)
        draw.fontmode = "0" #one sets to not antialias. If camera antialiases, set to zero.
        draw.text((1,1), self.letter, (255,255,255), font = self.font)
        self.letterImage = self.letterImg.load()
        #self.letterImg = GaussianBlur.getGaussianFilteredImage(self.letterImg, self.letterImage, 3)
    
        