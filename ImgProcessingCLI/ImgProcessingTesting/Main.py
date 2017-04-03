from PIL import Image
from ImgProcessingCLI.Testing import *
from ImgProcessingCLI.ImageOperation import get_img_scaled_to_one_bound
from PIL import ImageOps
import ImgProcessingCLI.ImageOperation.Mask as Mask
from ImgProcessingCLI.Color import *
#from ImgProcessingCLI.ImageSegmentation.LetterSegmenter import LetterSegmenter
import timeit
import os
from EigenFit import *
import ImgProcessingCLI.ImageOperation.ImageMath as ImageMath
from ImgProcessingCLI.DataMine.KMeansCompare import KMeansCompare
from EigenFit import *

from ImgProcessingCLI.EdgeProcessing.SobelEdge import SobelEdge
import ImgProcessingCLI.EdgeProcessing.CannyEdge as CannyEdge
import ImgProcessingCLI.NoiseReduction.GaussianBlur as GaussianBlur
import ImgProcessingCLI.ImageSegmentation.LetterSegmenter as LetterSegmenter
from ImgProcessingCLI.General.TargetTwo import TargetTwo
import timeit

'''
base_dir = "/Users/phusisian/Desktop/Senior year/SUAS/Generated Targets/Generated Targets Amble/Images"
img_files = os.listdir(base_dir)
remove_names_without_extension(img_files, 'png')
imgs = [Image.open(base_dir + "/" + img_files[i]).convert('RGB') for i in range(0, len(img_files))]
base_path = "/Users/phusisian/Desktop/Senior year/SUAS/Competition Files/NEWLETTERPCA"
eigenvectors = load_numpy_arr(base_path + "/Data/Eigenvectors/eigenvectors 0.npy")
projections_path = base_path + "/Data/Projections"
mean = load_numpy_arr(base_path + "/Data/Mean/mean_img 0.npy")
num_dim = 20
letter_categorizer = Categorizer(eigenvectors, mean, projections_path, KMeansCompare, 25)
for i in range(0, len(imgs)):
    start_time = timeit.default_timer()
    target = TargetTwo(imgs[i], imgs[i].load(), letter_categorizer)
    print(target)
    print("Finished in: " + str(timeit.default_timer() - start_time))
    print("-----------------------------------------------------")
'''

start_time = timeit.default_timer()
tester = SyntheticTester("/Users/phusisian/Desktop/Senior year/SUAS/Generated Targets/Generated Targets Amble/Images", "/Users/phusisian/Desktop/Senior year/SUAS/Generated Targets/Generated Targets Amble/Answers", 1, ".png")
print("final score: " + str(tester.get_score_vals()))
print("num crashed: " + str(tester.get_num_crashes()))
print("time elapsed: " + str(timeit.default_timer() - start_time))
