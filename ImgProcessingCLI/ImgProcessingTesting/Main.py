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
import ImgProcessingCLI.ImgStat.HistogramMaker as HistogramMaker

from scipy.signal import argrelextrema
#from mpl_toolkits.mplot3d import Axes3D
#import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import scipy
import ImgProcessingCLI.TargetTrait.FalseCropCatcher as FalseCropCatcher
from ImgProcessingCLI.Testing.FalseCropTester import FalseCropTester
import numpy

from ImgProcessingCLI.Runtime.RuntimeTarget import RuntimeTarget
from ImgProcessingCLI.Runtime.GeoStamps import GeoStamps
from ImgProcessingCLI.Runtime.GeoStamp import GeoStamp
#import exifread
from PIL import ExifTags
import ImgProcessingCLI.KernelOperations.ScaleSpace as ScaleSpace
import ImgProcessingCLI.KernelOperations.BlobDetect as BlobDetect
import ImgProcessingCLI.NoiseReduction.NeighborhoodReduction as NeighborhoodReduction
import cv2
import rawpy

from ImgProcessingCLI.Runtime.TargetCrop import TargetCrop
from ImgProcessingCLI.Runtime.RuntimeTarget import RuntimeTarget
import ImgProcessingCLI.Runtime.TargetCropper as TargetCropper
from ImgProcessingCLI.Testing.CropTester import CropTester




'''

img = Image.open("/Users/phusisian/Desktop/Senior year/SUAS/Object images/300.jpg")
base_path = "/Users/phusisian/Desktop/Senior year/SUAS/Competition Files/GENERATED FORCED WINDOW PCA"
orientation_path = "/Users/phusisian/Desktop/Senior year/SUAS/Competition Files/GENERATED 180 ORIENTATION PCA"

test_geo_stamps = GeoStamps([GeoStamp((10, 10), 500)], [GeoStamp((10, 10), 500)])
competition_solver = CompetitionInput("/Users/phusisian/Desktop/Senior year/SUAS/Competition Files/Competition Runtime Test", ".jpeg", base_path, 20, orientation_path, 50, test_geo_stamps)
'''


'''
start_time = timeit.default_timer()
base_path = "/Users/phusisian/Desktop/Senior year/SUAS/Generated Targets/BlockText 1000 Sets/Generated Targets BlockText 1000 A"#"/Users/phusisian/Desktop/Senior year/SUAS/Generated Targets/Generated Targets BlockText"#
tester = SyntheticTester(base_path + "/Images", base_path + "/Answers", 1, ".png")
score_vals = tester.get_score_vals()
total_score = numpy.sum(numpy.asarray(score_vals))
print("final score: " + str(tester.get_score_vals()))
print("% correct: " + str(100.0 * total_score/float(tester.get_score_denominator())))
print("num crashed: " + str(tester.get_num_crashes()))
print("time elapsed: " + str(timeit.default_timer() - start_time))
print("wrong score info: \n" + str(tester.get_wrong_score_info()))
'''

#cv_img = cv2.imread('/Users/phusisian/Dropbox/SUAS/Test sets/Crisp Real Flight Images/Crisp Img 1.SRW')
#cv2.imshow('hi', cv_img)




'''
path = '/Users/phusisian/Dropbox/SUAS/Test sets/Crisp Real Flight Images/Crisp Img 1.SRW'
raw = rawpy.imread(path)
rgb = raw.postprocess()



img = Image.fromarray(rgb).convert('RGB')#Image.open("/Users/phusisian/Dropbox/SUAS/Test sets/Crisp Real Flight Images/Crisp Img 1.SRW").convert('RGB')
#img.show()
'''

start_time = timeit.default_timer()
crop_tester = CropTester("/Users/phusisian/Dropbox/SUAS/Test sets/Full Synthetic Imgs/Generated_Targets_Full", ".png")
pos, false_neg, missing = crop_tester.test_set(250)
print("final scores: \n positives: ", pos, ", false negatives: ", false_neg, ", missing: ", missing)
print("time taken for crop tester to run: ", timeit.default_timer() - start_time)




'''
img = Image.open("/Users/phusisian/Dropbox/SUAS/Test sets/Full Synthetic Imgs/Generated_Targets_Full/Images/10.png")

test_geo_stamps = GeoStamps([GeoStamp((10, 10), 500), GeoStamp((10, 10), 500)])
#img = Image.open("/Users/phusisian/Dropbox/SUAS/Test sets/Full Synthetic Imgs/Generated_Targets_Full/Images/7.png")#("/Users/phusisian/Dropbox/SUAS/Test sets/False Positive Catcher Set/False Positives/FP2.JPG")#
img.show()
target_crops = TargetCropper.get_target_crops_from_img2(img, test_geo_stamps, 3.567)
for i in range(0, len(target_crops)):
    target_crops[i].get_crop_img().show()
'''
'''
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

full_img = Image.open("/Users/phusisian/Desktop/Senior year/SUAS/Object images/targets 400.JPG")
crop_img = Image.open("/Users/phusisian/Desktop/Senior year/SUAS/Object images/400 crop 6480x4320.jpg")
crop_loc = ( 3721 , 2468)
lat_long = (39.0458, 76.6413)
test_geo_stamps = GeoStamps([GeoStamp((10, 10), 500), GeoStamp((10, 10), 500)])
target_crop = TargetCrop(full_img, crop_img, test_geo_stamps, crop_loc, 3.567)
#print("target crop characteristics: ", target_crop)



runtime_targets = []
for i in range(0, len(target_crops)):
    append_runtime_target = RuntimeTarget(target_crops[i], letter_categorizer, orientation_solver)
    print("target ", i, ": ", append_runtime_target)
    runtime_targets.append(append_runtime_target)
'''


#target = RuntimeTarget(target_crop, letter_categorizer, orientation_solver)#TargetTwo.init_with_TargetCrop(target_crop, letter_categorizer, orientation_solver)
#print("target attributes: ", target.get_competition_json_output())


'''
false_crop_tester = FalseCropTester("/Users/phusisian/Dropbox/SUAS/Test sets/False Positive Catcher Set", 10, ".png", ".JPG")
false_neg, false_pos = false_crop_tester.run_imgs()
print("false negatives: ", false_neg, " false positives: ", false_pos)
'''
