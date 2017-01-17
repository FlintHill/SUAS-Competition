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
startTime = timeit.default_timer()

FONT_STRING = "Amble-Regular.ttf"

'''pentagonImg = Image.open("/Users/phusisian/Desktop/Senior year/SUAS/Object Images/hexagontest.jpg")
pentagonImage = pentagonImg.load()

pentagonImg = GrayScale.getGrayScaledImage(pentagonImg, pentagonImage)
pentaSobel = SobelEdge(pentagonImg, pentagonImage)
pentaCanny = CannyEdge.getCannyEdgeImage(pentaSobel, 40, 10)
pentaLine = HoughLine(pentaCanny, pentaCanny.load())
pentaLine.drawLinesOverThreshold(pentaCanny, pentaCanny.load(), 55, (255,0,0)).show()'''


#print(pentaLine)
#pentaLine.drawLinesOverThreshold(pentaCanny, pentaCanny.load(), 200)#drawHighestWeightPosition(pentaCanny, pentaCanny.load())
#pentaCanny.show()
#HarrisCorner.getCorners(pentaCanny, pentaCanny.load(), pentaSobel, 3, 5, 10000)
#pentaCanny.show()

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
print("time taken: " + str(timeit.default_timer() - startTime))