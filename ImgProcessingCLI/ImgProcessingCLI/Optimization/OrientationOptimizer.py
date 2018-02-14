import EigenFit.Load.NumpyLoader as NumpyLoader
import EigenFit.Vector.VectorMath as VectorMath
import EigenFit.Vector.EigenProjector as EigenProjector
import EigenFit.Load.FileFunctions as FileFunctions
import os
import string
from PIL import Image
import numpy

class OrientationOptimizer:
    def __init__(self, orientation_solver, testing_path, img_extension):
        self.img_extension = img_extension
        self.orientation_solver = orientation_solver
        self.testing_path = testing_path

    def get_test_score(self):
        test_imgs = []
        img_names = os.listdir(self.testing_path + "/Images")
        FileFunctions.remove_names_without_extension(img_names, self.img_extension)
        img_names = sorted(img_names, key = lambda name : int(name[0:name.index(".")]))
        for i in range(0, len(img_names)):
            test_imgs.append(Image.open(self.testing_path + "/Images/"  + img_names[i]).convert('L'))
        answer_key = list(NumpyLoader.load_numpy_arr(self.testing_path + "/Answers/answers.npy"))

        answers = []
        num_right = 0
        for i in range(0, len(test_imgs)):
            result = self.orientation_solver.get_letter_img_orientation(test_imgs[i])
            if result == answer_key[i]:
                num_right += 1
        return num_right
