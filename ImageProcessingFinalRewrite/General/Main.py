from Stat.EigenImageProjector import EigenImageProjector
from FileLoading.DataLoader import DataLoader
from PIL import Image
import NoiseReduction.GaussianBlur as GaussianBlur
from EdgeProcessing.SobelEdge import SobelEdge
import EdgeProcessing.CannyEdge as CannyEdge
from ImgStat.KMeans import KMeans
import Color.ColorMath as ColorMath
from Color.ColorSplitter import ColorSplitter
from General.Target import Target

shape_img = Image.open("/Users/phusisian/Desktop/Senior year/SUAS/Object images/400 crop triangle 6480x4320.jpg")
target = Target(shape_img, shape_img.load())

shape_img = shape_img.resize((50, 67))
data_path = "/Users/phusisian/Desktop/Senior year/SUAS/PCATesting/ManavImgs/Data"
data_loader = DataLoader(data_path, 40)
shape_eigen = EigenImageProjector(data_loader, shape_img.convert('L'))