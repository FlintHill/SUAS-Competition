from PIL import Image
from SyntheticDataset.image_operations import *
from SyntheticDataset.color import *
import math

ColorList()
#image = img.load()
#fieldObject = FieldObject("heptagon", Rectangle(0,0,100,100), math.pi/6.0, ColorList.getColorValueByName("orange"), "E")
#fieldObject.fill(img, image)
#img.swhow()
#print(fieldObject)
imageGen = ImageGenerator()
imageGen.fillPolyPics(1)
imageGen.savePolyPicImgs("/Users/vtolpegin/github/SUAS-Competition/SyntheticDataset/Generated_Targets")
#imageGen.getRandomlyGeneratedImg().show()
