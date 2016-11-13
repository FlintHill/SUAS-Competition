from PIL import Image
from KMeans import KMeans
from EdgeDetection import EdgeDetection
import ObjectDetection
import Rectangle
import Paint
import LetterFrame
import ShapeCharacteristics
import os
import LetterFrames
import CharacterCropper
import Line
import Point
import LineCaster
import timeit

img = Image.open("/Users/phusisian/Desktop/Senior year/SUAS/Object images/400 crop triangle 6480x4320.jpg")
#img.show()
image = img.load()
dim = img.size
kmeans= KMeans()
start = timeit.default_timer()
kmeansImg = kmeans.getKMeans(img, 3, 5)
print(timeit.default_timer()-start)
kmeansImg.show()

'''lFrames = LetterFrames.LetterFrames("Amble-Regular.ttf", 500)


kFrame = LetterFrame.LetterFrame("Y", "Amble-Regular.ttf", 200)
qFrame = LetterFrame.LetterFrame("R", "Amble-Regular.ttf", 100)
caster = LineCaster.LineCaster(LetterFrame.LetterFrame("Y", "Amble-Regular.ttf", 100).getImage())
caster.getSlopeImage().show()

print("least square: " + str(kFrame.getLeastSlopeSquare(qFrame.getLines())))

cc = CharacterCropper.CharacterCropper(kmeansImg)
imgs = cc.getSeparatedColorImages()
cc.getLetterCropImage().show()
cropImg = cc.getLetterCropImage()
print("crop square: " + str(qFrame.getLeastSlopeSquare(LineCaster.LineCaster(cropImg).getLines())))'''


