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
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import scipy
import ImgProcessingCLI.TargetTrait.FalseCropCatcher as FalseCropCatcher
from ImgProcessingCLI.Testing.FalseCropTester import FalseCropTester
import numpy

from ImgProcessingCLI.Runtime.RuntimeTarget import RuntimeTarget
from ImgProcessingCLI.Runtime.CompetitionInput import CompetitionInput
from ImgProcessingCLI.Runtime.GeoStamps import GeoStamps
from ImgProcessingCLI.Runtime.GeoStamp import GeoStamp
#import exifread
from PIL import ExifTags
import ImgProcessingCLI.KernelOperations.ScaleSpace as ScaleSpace
import ImgProcessingCLI.KernelOperations.BlobDetect as BlobDetect
import ImgProcessingCLI.NoiseReduction.NeighborhoodReduction as NeighborhoodReduction
import cv2

'''
false_crop_tester = FalseCropTester("/Users/phusisian/Dropbox/SUAS/Test sets/False Positive Catcher Set", 10, ".png", ".JPG")
false_neg, false_pos = false_crop_tester.run_imgs()
print("false negatives: ", false_neg, " false positives: ", false_pos)
'''



cv_img = cv2.imread('/Users/phusisian/Dropbox/SUAS/Test sets/Generated Targets BlockText 1000 A/Images/Generated Target 5.png')
colors = cv_img.reshape((-1, 3))
colors = numpy.float32(colors)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 3
ret,label,center=cv2.kmeans(colors,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
center = numpy.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((cv_img.shape))

cv2.imshow('res2',res2)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''cv2.imshow('dst_rt', cv_img)
cv2.waitKey(0)
cv2.destroyAllWindows()'''

'''
img = (Image.open("/Users/phusisian/Dropbox/SUAS/Test sets/Full Synthetic Imgs/Generated_Targets_Full/Images/0.png").convert('L')).resize((1620,1080))
#img = GaussianBlur.get_gaussian_filtered_bw_img(img, img.load(), 5, 1)
img_sobel = SobelEdge(img)
grad_mag_img = img_sobel.get_gradient_mag_img()
grad_mag_image = grad_mag_img.load()

sobel_mask = Image.new('L', grad_mag_img.size)
sobel_image = sobel_mask.load()
for i in range(0, sobel_mask.size[0]):
    for j in range(0, sobel_mask.size[1]):
        if grad_mag_image[i,j] < 15:
            sobel_image[i,j] = 255
sobel_mask.show()

grad_mag_img.show()

sobel_mask = NeighborhoodReduction.get_img_with_pixels_to_neighborhood_mode(sobel_mask, sobel_image, 3)
sobel_mask = NeighborhoodReduction.get_img_with_pixels_to_neighborhood_mode(sobel_mask, sobel_image, 3)
sobel_mask.show()
#CannyEdge.get_canny_img(img_sobel, (20, 40)).show()
gradient_mags = img_sobel.get_gradient_mags()
img = Image.fromarray(255*gradient_mags.T/numpy.amax(gradient_mags))
img = grad_mag_img
#img = NeighborhoodReduction.get_img_with_pixels_to_neighborhood_mode(img, img.load(), 5)
img.show()
start_time = timeit.default_timer()
space, t_key = ScaleSpace.get_gray_img_to_scale_space(sobel_mask.convert('L'), sobel_mask.convert('L').load(), 30, 18)
crops = BlobDetect.get_blob_crops_from_scale_space_imgs(sobel_mask, space, t_key, 2, 30, response_threshold = 120)
for i in range(0, len(crops)):
    #crops[i].show()
    if not FalseCropCatcher.get_if_is_false_positive(crops[i], crops[i].load(), min_area = 20, max_area = 800):
        crops[i].show()
print("time elapsed: ", timeit.default_timer() - start_time)
'''
'''
img = Image.open("/Users/phusisian/Desktop/Senior year/SUAS/Object images/300.jpg")
base_path = "/Users/phusisian/Desktop/Senior year/SUAS/Competition Files/GENERATED FORCED WINDOW PCA"
orientation_path = "/Users/phusisian/Desktop/Senior year/SUAS/Competition Files/GENERATED 180 ORIENTATION PCA"

test_geo_stamps = GeoStamps([GeoStamp((10, 10), 500)], [GeoStamp((10, 10), 500)])
competition_solver = CompetitionInput("/Users/phusisian/Desktop/Senior year/SUAS/Competition Files/Competition Runtime Test", ".jpeg", base_path, 20, orientation_path, 50, test_geo_stamps)
'''


'''
start_time = timeit.default_timer()
base_path = "/Users/phusisian/Desktop/Senior year/SUAS/Generated Targets/BlockText 1000 Sets/Generated Targets BlockText 1000 F"
tester = SyntheticTester(base_path + "/Images", base_path + "/Answers", 1, ".png")
score_vals = tester.get_score_vals()
total_score = numpy.sum(numpy.asarray(score_vals))
print("final score: " + str(tester.get_score_vals()))
print("% correct: " + str(100.0 * total_score/(5.0 * 1000.0)))
print("num crashed: " + str(tester.get_num_crashes()))
print("time elapsed: " + str(timeit.default_timer() - start_time))
print("wrong score info: \n" + str(tester.get_wrong_score_info()))
'''

'''
img = Image.open("/Users/phusisian/Dropbox/SUAS/Test sets/Real Targets/Real Target 1.jpg").convert('RGB').resize((45,45), Image.BICUBIV)
img.show()
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
'''
