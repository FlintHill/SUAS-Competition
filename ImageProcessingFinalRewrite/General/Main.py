#from Stat.EigenImageProjector import EigenImageProjector
#from FileLoading.DataLoader import DataLoader
from PIL import Image
import NoiseReduction.GaussianBlur as GaussianBlur
from EdgeProcessing.SobelEdge import SobelEdge
import EdgeProcessing.CannyEdge as CannyEdge
from ImgStat.KMeans import KMeans
import Color.ColorMath as ColorMath
from Color.ColorSplitter import ColorSplitter
from General.Target import Target
from DataMine.KNearestNeighbors import KNearestNeighbors
#from FileLoading.Categorizer import Categorizer
from Character.SWT import SWT
from PIL import ImageOps
import timeit
from DataMine.ZScore import ZScore
import EdgeProcessing.HarrisCorner as HarrisCorner
import Color.TargetColorReader as TargetColorReader
from Testing.SyntheticTester import SyntheticTester


tester = SyntheticTester("/Users/phusisian/Desktop/Senior year/SUAS/Generated Targets BlockText/Images", "/Users/phusisian/Desktop/Senior year/SUAS/Generated Targets BlockText/Answers", 1, ".png")
print("final score: " + str(tester.get_score_vals()))
print("num crashed: " + str(tester.get_num_crashes()))

