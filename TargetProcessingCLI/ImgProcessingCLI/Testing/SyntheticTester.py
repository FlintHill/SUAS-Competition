import os
import numpy
from PIL import Image
from ImgProcessingCLI.General import Target
from ImgProcessingCLI.DataMine import KMeansCompare
from EigenFit import *
import timeit
from NNet.Main.Layers import Layers
import NNet.Function.Cost as Cost
import NNet.Function.Sigmoid as Sigmoid

class SyntheticTester(object):
    def __init__(self, img_path_in, data_path_in, scale, extension):
        self.img_path = img_path_in
        self.data_path = data_path_in
        self.extension = extension

        print("categorizer initialization started")
        base_path = "/Users/phusisian/Desktop/Senior year/SUAS/Competition Files/NEWLETTERPCA"# WITH ROTATIONS"
        eigenvectors = NumpyLoader.load_numpy_arr(base_path + "/Data/Eigenvectors/eigenvectors 0.npy")
        projections_path = base_path + "/Data/Projections"
        mean = NumpyLoader.load_numpy_arr(base_path + "/Data/Mean/mean_img 0.npy")
        num_dim = 20
        nnet = Layers.init_from_files("/Users/phusisian/Desktop/Senior year/SUAS/NNet Files/Letter Weights 10 With Flipped Output", Sigmoid, [num_dim, 100, 27], Cost)
        self.letter_categorizer = Categorizer(eigenvectors, mean, projections_path, KMeansCompare, 25)
        print("categorizer initialization finished.")
        self.init_img_files()
        self.init_data_files()
        self.init_score_vals()
        self.check_answers(scale, extension)

    def init_img_files(self):
        self.img_files = os.listdir(self.img_path)
        i=0
        while i < len(self.img_files):
            if not self.img_files[i].endswith(self.extension):
                del self.img_files[i]
            else:
                i+=1
        print("img files: " + str(self.img_files))

    def init_data_files(self):
        self.data_files = os.listdir(self.data_path)
        i=0
        while i < len(self.data_files):
            if not self.data_files[i].endswith(".npy"):
                del self.data_files[i]
            else:
                i+=1
        print("data files: " + str(self.data_files))

    def init_score_vals(self):
        self.score_vals = numpy.zeros((5))

    def check_answers(self, scale, extension):
        self.num_crashes = 0
        for i in range(0, len(self.img_files)):
            try:
                start_time = timeit.default_timer()
                shape_img = Image.open(self.img_path + "/" + str(self.img_files[i]))#Image.open(self.img_path + "/Generated Target " + str(i) + extension)

                end_num = self.get_file_name_end_num(self.img_files[i])
                matching_data_file_name = self.get_data_file_name_with_end_num(end_num)
                scores = numpy.load(self.data_path + "/" + matching_data_file_name)

                shape_img = shape_img.resize((int(shape_img.size[0]*scale), int(shape_img.size[1]*scale)))
                target = Target(shape_img, shape_img.load(), self.letter_categorizer)
                target_answers = target.as_numpy()

                if str(scores[0]) == str(target_answers[0]):
                    self.score_vals[0] += 1
                elif self.get_if_letter_is_bidirectional(str(scores[3])):
                    flipped_angle = self.get_compass_angle_180_degrees_away(str(target_answers[0]))
                    if str(flipped_angle) == str(scores[0]):
                        self.score_vals[0] += 1
                print("=============================================================")
                print("answer key: " + str(scores))
                print("target answers: " + str(target_answers))
                for answer_index in range(1, scores.shape[0]):
                    if str(target_answers[answer_index]) == str(scores[answer_index]):
                        self.score_vals[answer_index] += 1
                print("current score vals: " + str(self.score_vals) + ", num images run: " + str(i+1))
                print("time taken: " + str(timeit.default_timer() - start_time) + " seconds")
                print("=============================================================")
                print("------------------------------------------------------------")
            except:
                self.num_crashes += 1
                print("done messt up")

    def get_file_name_end_num(self, img_name):
        space_index = img_name.rfind(" ")
        dot_index = img_name.rfind(".")
        num_string = img_name[space_index + 1: dot_index]
        return int(num_string)

    def get_data_file_name_with_end_num(self, num):
        for i in range(0, len(self.data_files)):
            if num == self.get_file_name_end_num(self.data_files[i]):
                return self.data_files[i]
        return None

    def get_if_letter_is_bidirectional(self, letter):
        return (letter == "H" or letter == "I" or letter == "N" or letter == "O" or letter == "S" or letter == "X" or letter == "Z")

    def get_compass_angle_180_degrees_away(self, compass_dir):
        if compass_dir == "N":
            return "S"
        if compass_dir == "NE":
            return "SW"
        if compass_dir == "E":
            return "W"
        if compass_dir == "SE":
            return "NW"
        if compass_dir == "S":
            return "N"
        if compass_dir == "SW":
            return "NE"
        if compass_dir == "W":
            return "E"
        return "SE"

    def get_score_vals(self):
        return self.score_vals

    def get_num_crashes(self):
        return self.num_crashes
