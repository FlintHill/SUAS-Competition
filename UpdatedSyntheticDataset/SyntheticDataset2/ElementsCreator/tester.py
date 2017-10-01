from SyntheticDataset2.ElementsCreator import *
import numpy
from PIL import Image, ImageDraw
import sys
import subprocess
import time

img = Image.new('RGBA', (500,500), color=(0,0,255))


#rectangle = Rectangle(100, 50, (255,0,0), (250,250), 45, img)
#rectangle.overlay()

#triangle = Triangle(100, 100, (255,0,0), (250,250), 33, img)
#triangle.overlay()

#circle = Circle(100, (255,0,0), (250,250), img)
#circle.overlay()

#half_circle = HalfCircle(100, (255,0,0), (250,250), 45, img)
#half_circle.overlay()

#square = Square(100, (255,0,0), (250,250), 45, img)
#square.overlay()

#trapezoid = Trapezoid(100,50,25,(255,0,0),(250,250),45,img)
#trapezoid.overlay()

#quarter_circle = QuarterCircle(50, (255,0,0), (250,250), 33, img)
#quarter_circle.overlay()

#cross = Cross(50,(255,0,0),(250,250),45,img)
#cross.overlay()

img.show()
