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
startTime = timeit.default_timer()

'''
circleImg = LetterFrame("D", "Amble-Regular.ttf", (150)).getLetterImg()#circleImg = Image.open("/Users/phusisian/Desktop/Senior year/SUAS/Object images/circles-002.jpg")
circleImage = circleImg.load()
circleImg = GrayScale.getGrayScaledImage(circleImg, circleImage)
circleImg = GaussianBlur.getGaussianFilteredImg(circleImg, circleImage, 3, 2)
circleSobel = SobelEdge(circleImg, circleImage)
circleImg = CannyEdge.getCannyEdgeImage(circleSobel, 40, 10)
circleImage = circleImg.load()
circleHoughs = HoughCircles(circleImg, circleImage, (15, 50))
circleHoughs.circleCirclesOverThreshold(circleImg, circleImage, 30).show()
circleImg.show()
'''

#highestCirclePoint = circleHoughs.getHighestRadiusVotePoint()
#Drawer.drawCircle(circleImg, circleImage, Point(highestCirclePoint[0], highestCirclePoint[1]), highestCirclePoint[2], (255,0,0))
#drawRect = Rectangle(highestCirclePoint[0] - 10, highestCirclePoint[1]-10, 20, 20)
#Drawer.fillRect(circleImg, circleImage, drawRect, (255,0,0))


'''
babyImg = Image.open("/Users/phusisian/Desktop/Senior year/SUAS/Object images/BabyTestPic2.jpg")
babyImage = babyImg.load()
babyImg = GrayScale.getGrayScaledImage(babyImg, babyImage)
babyImg = GaussianBlur.getGaussianFilteredImg(babyImg, babyImg.load(), 7, 20)
sobelEdge = SobelEdge(babyImg, babyImage)
sobelEdge.getAngleImage(0).show()'''
'''
aFrame = LetterFrame("Q", "Amble-Regular.ttf", 60)
aImg = aFrame.getLetterImg()
aImage = aImg.load()
#aImg = GaussianBlur.getGaussianFilteredImg(aImg, aImage, 5, 5)
HarrisCorner.getCorners(aImg, aImage, SobelEdge(aImg, aImage), 3, 5, 750000)
aImg.show()   ''' 


imageFinder = ImageFinder("/Users/phusisian/Desktop/Senior year/SUAS/Generated Targets", ".png")
imageFinder.waitUntilImagePresent()
imageFinder.printDir()
imgPaths = imageFinder.getImgPaths()

scaleRatio = LetterFrame.getHeightToFontRatio("Amble-Regular.ttf")
frames = LetterFrames("Amble-Regular.ttf", 58)
#Try to MAKE letter frames GIVEN the letter. They actually build fairly fast now, so that isn't too bad. 
#this will solve the image scaling problems.
fontFitter = FontFitter("Amble-Regular.ttf", (50, 70))
print("font it think itbe!: " + str(fontFitter.getBestFittingFontForSize(frames.getFrameHeight())))
secondFrames = LetterFrames("Amble-Regular.ttf", fontFitter.getBestFittingFontForSize(frames.getFrameHeight()))
#secondFrames = LetterFrames("Amble-Regular.ttf", int(frames.getFrameHeight() * scaleRatio))#LetterFrames("Amble-Regular.ttf", 36)#frames#


'''
for i in range(0, len(frames)):
    letterImg = frames[i].getLetterImg()
    compareFrame = LetterFrame(frames[i].getLetter(), "Amble-Regular.ttf", 64)
    letterClusterer = LetterClusterer(letterImg, 12)
    compareClusterer = LetterClusterer(compareFrame.getLetterImg(), 12)
    letterClusterer.getImgWithClusters().show()
    cls = ClusterLeastSquare((letterImg.size[0]/2, letterImg.size[1]/2), letterClusterer.getClusters(), (letterImg.size[0]/2, letterImg.size[1]/2), compareClusterer.getClusters())
    
    randFrame = frames[randint(0,24)]
    randomLetterImg = randFrame.getLetterImg()
    randomClusterer = LetterClusterer(randomLetterImg, 12)
    clsWrong = ClusterLeastSquare((randomLetterImg.size[0]/2, randomLetterImg.size[1]/2), randomClusterer.getClusters(), (letterImg.size[0]/2, letterImg.size[1]/2), compareClusterer.getClusters())
    
    print("Letter: " + compareFrame.getLetter() + "\n" + str(cls))
    print()
    print("WRONG COMPARE LETTER: " + randFrame.getLetter() + " actual letter: " + compareFrame.getLetter() + "\n" + str(clsWrong))
    print()'''

'''babyImg = Image.open("/Users/phusisian/Desktop/Senior year/SUAS/Object images/plaid mid res.jpg")
babyImage = babyImg.load()
babyImg = GrayScale.getGrayScaledImage(babyImg, babyImage)
babyImg = GaussianBlur.getGaussianFilteredImg(babyImg, babyImage, 5, 10)
babyImage = babyImg.load()
HarrisCorner.getCorners(babyImg, babyImage, SobelEdge(babyImg, babyImage), 5, 5, 750000)'''
    
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