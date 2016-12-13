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

#img = Image.open("/Users/phusisian/Desktop/Senior year/SUAS/Object images/300 crop 6480x4320.jpeg")
#image = img.load()

startTime = timeit.default_timer()


imageFinder = ImageFinder("/Users/phusisian/Desktop/Senior year/SUAS/Object images test", ".jpeg")
imageFinder.waitUntilImagePresent()
imageFinder.printDir()
imgPaths = imageFinder.getImgPaths()

for filepath in imgPaths:
    img = Image.open(filepath)
    image = img.load()
    fieldObject = FieldObject(img, image)
    fieldObject.getColorLayers().printLayerDistancesToCorner()
    fieldObject.getLetterLayerCrappyVersion().getColorImg().show()
    print(fieldObject)

#kMeansImg.show()
#letterFrames = LetterFrames("Dual-300.ttf", 49)##instead of scaling letter to fit frame, you need to have frames that fit the letter
'''fieldObject = FieldObject(img, image)
fieldObject.getColorLayers().printLayerDistancesToCorner()
fieldObject.getLetterLayerCrappyVersion().getColorImg().show()
print(fieldObject)'''
#print("Letter: " + str(letterFrames.getBestFitLetterFrameFromSobel(fieldObject.getLetterSobel(), 0).getLetter()))
#bFrame = LetterFrame("B", "Amble-Regular.ttf", 124)
#letterFrames.getBestFitLetterFrameFromSobel(bFrame.getSobelEdge(), 45).showLetterImg()
#IDEA: For letter recognition, maybe use KMeans to get points of concentration then compare their location (sort for least fit distance). Another advantage is being able to grade it off things relative to image width and size
#print(fieldObject.getObjectColorName())
#fieldObject.getLetterColorLayer()
#fieldObject.showLayerImg()  
print("time taken: " + str(timeit.default_timer() - startTime))

#print(kMeans)

'''
grayImg = GrayScale.getGrayScaledImage(img, image)
gaussianImg = GaussianBlur.getGaussianFilteredImage(grayImg, grayImg.load(), 3)
sobelEdge = SobelEdge(gaussianImg, gaussianImg.load())
normalFontFrames = LetterFrames("Amble-Regular.ttf", 124)
comicSansFontFrames = LetterFrames("abeezee.regular.ttf", 124)
sobelEdge.getSobelEdgeImg().show()
sobelEdge.getAngleImage(0).show()
CannyEdge.getCannyEdgeImage(sobelEdge, 25, 8).show()

startTime = timeit.default_timer()
print("Accuracy: " + str(normalFontFrames.checkAccuracyUsingLeastSquare(comicSansFontFrames, 45)))
print("Time Taken: " + str(timeit.default_timer() - startTime))'''