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

from sklearn.datasets import load_iris
from sklearn import tree
from sklearn import ensemble

'''
base_path = "/Users/phusisian/Desktop/Senior year/SUAS/Competition Files/NEWLETTERPCA"
eigenvectors = load_numpy_arr(base_path + "/Data/Eigenvectors/eigenvectors 0.npy")
projections_path = base_path + "/Data/Projections"
mean = load_numpy_arr(base_path + "/Data/Mean/mean_img 0.npy")
num_dim = 20
letter_categorizer = Categorizer(eigenvectors, mean, projections_path, KMeansCompare, num_dim)
named_projections = letter_categorizer.get_named_projections()

data = []
targets = []
for i in range(0, len(named_projections)):
    projections = named_projections[i].get_projections()
    for j in range(0, len(projections)):
        data.append(projections[j])
        targets.append(i)


rand_training_data = []
rand_training_targets = []
rand_testing_data = []
rand_testing_targets = []
for i in range(0, len(data)):
    if random.random() > 0.2:
        rand_training_data.append(data[i])
        rand_training_targets.append(targets[i])
    else:
        rand_testing_data.append(data[i])
        rand_testing_targets.append(targets[i])

classifier = ensemble.RandomForestClassifier()
classifier = classifier.fit(rand_training_data, rand_training_targets)
predictions = classifier.predict(rand_testing_data)

num_right = 0
for i in range(0, len(predictions)):
    if predictions[i] == rand_testing_targets[i]:
        num_right += 1

print("percent right: " + str(float(num_right)/float(len(predictions))))
'''

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
base_path = "/Users/phusisian/Desktop/Senior year/SUAS/Generated Targets/Generated Targets BlockText"
tester = SyntheticTester(base_path + "/Images", base_path + "/Answers", 1, ".png")
print("final score: " + str(tester.get_score_vals()))
print("num crashed: " + str(tester.get_num_crashes()))
print("time elapsed: " + str(timeit.default_timer() - start_time))
