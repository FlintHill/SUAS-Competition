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
import random
from ImgProcessingCLI.Optimization.LetterGenerator import LetterGenerator
from ImgProcessingCLI.Optimization.Optimizer import Optimizer

from sklearn.datasets import load_iris
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn import ensemble
from ImgProcessingCLI.Optimization.OrientationOptimizer import OrientationOptimizer
from ImgProcessingCLI.DataMine.OrientationSolver import OrientationSolver

'''
set_gen = LetterGenerator("/Users/phusisian/Desktop/Senior year/SUAS/PCATesting/SUASLetterImgs/Imgs", ".png")
#set_gen.generate_training_set("/Users/phusisian/Desktop/Senior year/SUAS/PCATesting/Generated Letter Sets/Generated Set 1/Training", 120)
#set_gen.generate_orientation_test_set("/Users/phusisian/Desktop/Senior year/SUAS/Generated Targets/LetterSetOrientation", 5000)
set_gen.generate_test_set("/Users/phusisian/Desktop/Senior year/SUAS/Generated Targets/LetterSet", 5000)
'''
'''
base_path = "/Users/phusisian/Desktop/Senior year/SUAS/Competition Files/GENERATED FORCED WINDOW PCA"
eigenvectors = NumpyLoader.load_numpy_arr(base_path + "/Data/Eigenvectors/eigenvectors 0.npy")
mean_img_vector = NumpyLoader.load_numpy_arr(base_path + "/Data/Mean/mean_img 0.npy")
optimizer = Optimizer(KNeighborsClassifier(n_neighbors = 5), base_path, "/Users/phusisian/Desktop/Senior year/SUAS/Generated Targets/LetterSet", 20, ".png")
print("score: ", optimizer.get_test_score())
'''

'''
orientation_path = "/Users/phusisian/Desktop/Senior year/SUAS/Competition Files/GENERATED 180 ORIENTATION PCA"
orientation_eigenvectors = load_numpy_arr(orientation_path + "/Data/Eigenvectors/eigenvectors 0.npy")
orientation_projections_path = orientation_path + "/Data/Projections"
orientation_mean = load_numpy_arr(orientation_path + "/Data/Mean/mean_img 0.npy")
orientation_num_dim = 20
orientation_solver = OrientationSolver(orientation_eigenvectors, orientation_mean, orientation_path, orientation_num_dim)
orientation_optimizer = OrientationOptimizer(orientation_solver, "/Users/phusisian/Desktop/Senior year/SUAS/Generated Targets/LetterSetOrientation", ".png")
print("score: ", orientation_optimizer.get_test_score())
'''

'''
start_time = timeit.default_timer()
base_path = "/Users/phusisian/Desktop/Senior year/SUAS/Generated Targets/Generated Targets Amble Big"
tester = SyntheticTester(base_path + "/Images", base_path + "/Answers", 1, ".png")
score_vals = tester.get_score_vals()
total_score = numpy.sum(numpy.asarray(score_vals))
print("final score: " + str(tester.get_score_vals()))
print("% correct: " + str(100.0 * total_score/(5.0 * 1000.0)))
print("num crashed: " + str(tester.get_num_crashes()))
print("time elapsed: " + str(timeit.default_timer() - start_time))
print("wrong score info: \n" + str(tester.get_wrong_score_info()))
'''


img = Image.open("/Users/phusisian/Desktop/Senior year/SUAS/Object images test/300 crop 6480x4320.jpeg").convert('RGB')
base_path = "/Users/phusisian/Desktop/Senior year/SUAS/Competition Files/GENERATED FORCED WINDOW PCA"
eigenvectors = load_numpy_arr(base_path + "/Data/Eigenvectors/eigenvectors 0.npy")
projections_path = base_path + "/Data/Projections"
mean = load_numpy_arr(base_path + "/Data/Mean/mean_img 0.npy")
num_dim = 20

letter_categorizer = Categorizer(eigenvectors, mean, projections_path, KMeansCompare, num_dim)


orientation_path = "/Users/phusisian/Desktop/Senior year/SUAS/Competition Files/GENERATED 180 ORIENTATION PCA"
orientation_eigenvectors = load_numpy_arr(orientation_path + "/Data/Eigenvectors/eigenvectors 0.npy")
orientation_projections_path = orientation_path + "/Data/Projections"
orientation_mean = load_numpy_arr(orientation_path + "/Data/Mean/mean_img 0.npy")
orientation_num_dim = 50

orientation_solver = OrientationSolver(orientation_eigenvectors, orientation_mean, orientation_path, orientation_num_dim)
target = TargetTwo(img, img.load(), letter_categorizer, orientation_solver)
print("target attributes: ", target)
