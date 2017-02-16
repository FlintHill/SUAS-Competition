from root.nested.SobelEdge import SobelEdge
from PIL import Image
from root.nested.GrayScale import GrayScale
from root.nested.GaussianBlur import GaussianBlur
from root.nested.CannyEdge import CannyEdge
from root.nested.LetterFrame import LetterFrame
from root.nested.LetterFrames import LetterFrames
from root.nested.FieldObject import FieldObject
from root.nested.KMeans import KMeans
from root.nested.ImageFinder import ImageFinder
import timeit
from root.nested.LetterClusterer import LetterClusterer
from root.nested.ClusterLeastSquare import ClusterLeastSquare
from random import randint
from root.nested.ClusterLeastSquare import ClusterSquareFitter
from root.nested.HarrisCorner import HarrisCorner
from root.nested.HoughCircles import HoughCircles
from root.nested.Rectangle import Rectangle
from root.nested.Drawer import Drawer
from root.nested.Point import Point
from root.nested.FontFitter import FontFitter
from root.nested.HoughLine import HoughLine
from root.nested.SWT import SWT
from root.nested.PictureMatrix import PictureMatrix
from root.nested.CovarianceMatrix import CovarianceMatrix
from root.nested.Stat import Stat
from root.nested.PolarSideCounter import PolarSideCounter
startTime = timeit.default_timer()
    

shapeImg = Image.open("/Users/phusisian/Desktop/Senior year/SUAS/Object images/squaretest.jpg")
shapeImg = shapeImg.resize((shapeImg.size[0]/4, shapeImg.size[1]/4))
#shapeImg = shapeImg.rotate(-10)
shapeImage = shapeImg.load()
shapeImg = GrayScale.getGrayScaledImage(shapeImg, shapeImage)
shapeImg = GaussianBlur.getGaussianFilteredImg(shapeImg, shapeImage, 5, 2)
shapeImage = shapeImg.load()
shapeImg.show()
shapeSobel = SobelEdge(shapeImg, shapeImage)

shapeCannyImg = CannyEdge.getCannyEdgeImage(shapeSobel, 40, 10)
shapeCannyImg = shapeCannyImg.rotate(0, expand=True)
shapeCannyImg.show()

polarSideCounter = PolarSideCounter(shapeCannyImg, shapeCannyImg.load())

'''

FONT_STRING = "Amble-Regular.ttf"
oFrame = LetterFrame("G", FONT_STRING, 100)
oFrame.getLetterImg().show()
oFrame.getSobelEdge().getSobelEdgeImg().show()
oFrame.getCannyImg().show()
swt = SWT(oFrame.getSobelEdge(), oFrame.getCannyImg(), oFrame.getCannyImg().load())
swtimg = swt.getFrameImg((0,0,255))
swtimg.show()

oMatrix = PictureMatrix(swtimg, swtimg.load())
covarMatrix = oMatrix#CovarianceMatrix(oMatrix)
eigenvectors = Stat.get2dEigenvectors(covarMatrix)
center = (oFrame.getCannyImg().size[0]/2, oFrame.getCannyImg().size[1]/2)
print("Eigenvectors: " + str(eigenvectors))
for i in range(0, len(eigenvectors)):
    eigenvectors[i] *= 10
    eigenvectors[i].draw2D(oFrame.getCannyImg(), oFrame.getCannyImg().load(), (int(covarMatrix.getMeans()[0] + center[0]), int(covarMatrix.getMeans()[1] + center[1])),(255,0,0))
oFrame.getCannyImg().show()


penImg = Image.open("/Users/phusisian/Desktop/Senior year/SUAS/Object images/Pen.jpg")
penImage = penImg.load()
penImg = GaussianBlur.getGaussianFilteredImg(penImg, penImage, 5, 7)
penImage = penImg.load()
penSobel = SobelEdge(penImg, penImage)
penCannyImg = CannyEdge.getCannyEdgeImage(penSobel, 16, 8)
penCannyImg.show()
penMatrix = PictureMatrix(penCannyImg, penCannyImg.load())
penCovariance = CovarianceMatrix(penMatrix)
penEigenvectors = Stat.get2dEigenvectors(penCovariance)
print("Eigenvectors: " + str(penEigenvectors))
center = (penCannyImg.size[0]/2, penCannyImg.size[1]/2)
for i in range(0, len(penEigenvectors)):
    penEigenvectors[i] *= 100
    penEigenvectors[i].draw2D(penCannyImg, penCannyImg.load(), (int(penCovariance.getMeans()[0] + center[0]), int(penCovariance.getMeans()[1] + center[1])), (255,0,0))

penCannyImg.show()






'''
'''reminder to threshold canny'''











'''

imageFinder = ImageFinder("/Users/phusisian/Desktop/Senior year/SUAS/Generated Targets", ".png")
imageFinder.waitUntilImagePresent()
imageFinder.printDir()
imgPaths = imageFinder.getImgPaths()

for i in range(0, len(imageFinder.getImgPaths())):
    iterImg = Image.open(imageFinder.getImgPaths()[i])
    iterImage = iterImg.load()
    iterKMeans = KMeans.initWithPicture(iterImg, iterImage, 3, 50, 1)
    iterImg = iterKMeans.filterImageThroughClusters(iterImg, iterImage)
    iterImage = iterImg.load()
    iterImg.show()
    iterImg = GrayScale.getGrayScaledImage(iterImg, iterImage)
    iterImage = iterImg.load()
    
    #iterImg = GaussianBlur.getGaussianFilteredImg(iterImg, iterImage, 3, 10)
    #iterImage = iterImg.load()
    imgSobel = SobelEdge(iterImg, iterImage)
    cannyImg = CannyEdge.getCannyEdgeImage(imgSobel, 40, 20)
    iterLines = HoughLine(cannyImg, cannyImg.load())
    iterLines.drawLinesOverThreshold(cannyImg, cannyImg.load(), 25, (255,0,0)).show()

frames = LetterFrames(FONT_STRING, 36)
fontFitter = FontFitter(FONT_STRING, (30, 40))
fitFontSize = fontFitter.getBestFittingFontForSize(frames.getFrameHeight())
print("Fit Font Size: " + str(fitFontSize))
secondFrames = LetterFrames(FONT_STRING, fitFontSize)
squareFitter = ClusterSquareFitter(frames)
numCorrect = 0
for i in range(0, len(frames)):
    checkLetter = frames[i].getLetter()
    answerLetter = squareFitter.getBestFitAvgLetter(secondFrames[i].getLetterImg())
    if checkLetter == answerLetter:
        numCorrect += 1
    print("Letter: " + checkLetter + " Answer: " + answerLetter + " Correct? " + str(checkLetter == answerLetter))

print("Accuracy: " + str(float(numCorrect/26.0)*100) + "%")
print("time taken: " + str(timeit.default_timer() - startTime))'''