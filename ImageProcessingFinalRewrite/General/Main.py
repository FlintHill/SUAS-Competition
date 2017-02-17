from PIL import Image
import NoiseReduction.GaussianBlur as GaussianBlur
from EdgeProcessing.SobelEdge import SobelEdge
import EdgeProcessing.CannyEdge as CannyEdge
from Stat.KMeans import KMeans
import Color.ColorMath as ColorMath
from Color.ColorSplitter import ColorSplitter
from General.Target import Target
#
shape_img = Image.open("/Users/phusisian/Desktop/Senior year/SUAS/Object images/400 crop 6480x4320.jpg")
#shape_img = shape_img.resize(((shape_img.size[0]/4), (shape_img.size[1]/4)))
target = Target(shape_img, shape_img.load())
