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



'''gaussian_target_img = Image.open("/Users/phusisian/Desktop/Senior year/SUAS/Generated Targets Amble/Images/Generated Target 0.png").convert('L')
start_time = timeit.default_timer()
for i in range(0, 10):
    gaussian_target_img = GaussianBlur.get_gaussian_filtered_bw_img(gaussian_target_img, gaussian_target_img.load(), 3, 1.0)
    gaussian_target_img = gaussian_target_img.resize((int(gaussian_target_img.size[0]*.9), int(gaussian_target_img.size[1]*.9)))
    #gaussian_target_img.show()
print("time taken: " + str(timeit.default_timer() - start_time))
gaussian_target_img.show()
'''

start_time = timeit.default_timer()
tester = SyntheticTester("/Users/phusisian/Desktop/Senior year/SUAS/Generated Targets Amble/Images", "/Users/phusisian/Desktop/Senior year/SUAS/Generated Targets Amble/Answers", 1, ".png")
print("final score: " + str(tester.get_score_vals()))
print("num crashed: " + str(tester.get_num_crashes()))
print("time elapsed: " + str(timeit.default_timer() - start_time))
