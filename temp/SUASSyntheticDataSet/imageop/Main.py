from PIL import Image
from imageop.ImageLoader import ImageLoader
from imageop.GradientMaker import GrayGradientMaker
from imageop.Polygon import Polygon
from imageop.Point import Point
from imageop.SimplePolygonMaker import SimplePolygonMaker
import math
from imageop.Rectangle import Rectangle
from imageop.FieldObject import FieldObject
from imageop.GaussianBlur import GaussianBlur
from imageop.FieldObject import ObjectLetter
from colorop.ColorList import ColorList
from imageop.ImageGenerator import ImageGenerator

ColorList()
#image = img.load()
#fieldObject = FieldObject("heptagon", Rectangle(0,0,100,100), math.pi/6.0, ColorList.getColorValueByName("orange"), "E")
#fieldObject.fill(img, image)
#img.swhow()
#print(fieldObject)
imageGen = ImageGenerator()
imageGen.fillPolyPics(50)
imageGen.savePolyPicImgs("/Users/phusisian/Desktop/Senior year/SUAS/Generated Targets/Generated Targets BlockText Blurry Grass")
#imageGen.getRandomlyGeneratedImg().show()