import os
import numpy
from PIL import Image
from ImgProcessingCLI import *
from EigenFit import *
import timeit

class SyntheticTester(object):

    def __init__(self, img_path_in, data_path_in, scale, extension):
        self.img_path = img_path_in
        self.data_path = data_path_in
        self.extension = extension
        self.scale = scale

        self.init_img_files()
        self.init_data_files()
        self.init_score_vals()

        print("categorizer initialization started")
        base_path = "/Users/vtolpegin/Desktop/SUAS/NEWLETTERPCA"
        eigenvectors = load_numpy_arr(base_path + "/Data/Eigenvectors/eigenvectors 0.npy")
        projections_path = base_path + "/Data/Projections"
        mean = load_numpy_arr(base_path + "/Data/Mean/mean_img 0.npy")
        num_dim = 20
        self.letter_categorizer = Categorizer(eigenvectors, mean, projections_path, KMeansCompare, 25)
        print("categorizer initialization finished.")

        self.test_set()

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

    def test_set(self):
        self.num_crashes = 0
        for index in range(0, len(self.img_files)):
            try:
                self.run_img(index)
            except:
                self.num_crashes += 1
                print("Crashed during test_set() on img", self.img_files[index])

    def run_img(self, index):
        """
        Process an image

        :param index: The index of the image in self.img_files
        :type index: int
        """
        start_time = timeit.default_timer()
        shape_img = Image.open(self.img_path + "/" + str(self.img_files[index]))

        end_num = self.get_file_name_end_num(self.img_files[index])
        matching_data_file_name = self.get_data_file_name_with_end_num(end_num)
        scores = numpy.load(self.data_path + "/" + matching_data_file_name)

        shape_img = shape_img.resize((int(shape_img.size[0]*self.scale), int(shape_img.size[1]*self.scale)))
        target = Target(shape_img, shape_img.load(), self.letter_categorizer)
        target_answers = target.as_numpy()

        if str(scores[0].decode("utf-8")) == str(target_answers[0]):
            self.score_vals[0] += 1
        elif self.get_if_letter_is_bidirectional(str(scores[3])):
            flipped_angle = self.get_compass_angle_180_degrees_away(str(target_answers[0]))
            if str(flipped_angle) == str(scores[0]):
                self.score_vals[0] += 1
        print("=============================================================")
        print("answer key: " + str(scores))
        print("target answers: " + str(target_answers))
        for answer_index in range(1, scores.shape[0]):
            if str(target_answers[answer_index].decode("utf-8")) == str(scores[answer_index]):
                self.score_vals[answer_index] += 1
        print("current score vals: " + str(self.score_vals) + ", num images run: " + str(index+1))
        print("time taken: " + str(timeit.default_timer() - start_time) + " seconds")
        print("=============================================================")
        print("------------------------------------------------------------")

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
