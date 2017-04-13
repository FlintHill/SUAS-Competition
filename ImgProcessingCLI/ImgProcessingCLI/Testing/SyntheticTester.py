import os
import numpy
from PIL import Image
from ImgProcessingCLI import *
from EigenFit import *
import timeit


from ImgProcessingCLI.DataMine.KNearestNeighbors import KNearestNeighbors
from ImgProcessingCLI.DataMine.ZScore import ZScore
from ImgProcessingCLI.General.TargetTwo import TargetTwo
from ImgProcessingCLI.Optimization.Optimizer import Optimizer
from ImgProcessingCLI.DataMine.OrientationSolver import OrientationSolver
from sklearn.neighbors import KNeighborsClassifier
from ImgProcessingCLI.General.TargetFunneler import TargetFunneler

class SyntheticTester(object):

    def __init__(self, img_path_in, data_path_in, scale, extension):
        self.img_path = img_path_in
        self.data_path = data_path_in
        self.extension = extension
        self.scale = scale

        self.init_img_files()
        self.init_data_files()
        self.init_score_vals()
        self.target_funneler = TargetFunneler("/Users/phusisian/Desktop/Senior year/SUAS/Competition Files/GENERATED FORCED WINDOW PCA", 20, "/Users/phusisian/Desktop/Senior year/SUAS/Competition Files/GENERATED 180 ORIENTATION PCA", 50)

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
        self.wrong_scores = [[] for i in range(0, 5)]

    def test_set(self):
        self.num_crashes = 0
        for index in range(0, len(self.img_files)):
            #try:
            self.run_img(index)
        #    except:
        #        self.num_crashes += 1
        #        print("Crashed during test_set() on img", self.img_files[index])


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
        target = self.target_funneler.init_target(shape_img.convert('RGB'))#TargetTwo(shape_img.convert('RGB'), shape_img.convert('RGB').load(), self.letter_categorizer, self.orientation_solver)#Target(shape_img, shape_img.load(), self.letter_categorizer)
        target_answers = target.as_numpy()
        str_scores = [scores[i].decode("utf-8") for i in range(0, len(scores))]


        if str(scores[0].decode("utf-8")) == str(target_answers[0]):
            self.score_vals[0] += 1
        elif self.get_if_letter_is_bidirectional(str_scores[3]):
            flipped_angle = self.get_compass_angle_180_degrees_away(str(target_answers[0]))
            if str(flipped_angle) == str_scores[0]:
                self.score_vals[0] += 1
            else:
                self.wrong_scores[0].append(("Correct answer: " + str(str_scores[0]), "Actual answer: " + str(target_answers[0])))
        else:
            self.wrong_scores[0].append(("Correct answer: " + str(str_scores[0]), "Actual answer: " + str(target_answers[0])))
        print("=================================================================================")



        print("answer key: " + str(str_scores))
        print("target answers: " + str(target_answers))
        for answer_index in range(1, scores.shape[0]):
            if str(target_answers[answer_index]) == str(scores[answer_index].decode("utf-8")):
                self.score_vals[answer_index] += 1
            else:
                self.wrong_scores[answer_index].append(("Correct answer: " + str(str_scores[answer_index]), "Actual answer: " + str(target_answers[answer_index])))
        print("current score vals: " + str(self.score_vals) + ", num images run: " + str(index+1))
        print("time taken: " + str(timeit.default_timer() - start_time) + " seconds")
        #print("wrong score info: \n", self.get_wrong_score_info())
        print("=================================================================================")
        print("---------------------------------------------------------------------------------")

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

    def get_wrong_score_info(self):
        out_strs = ["Orientation errors: \n", "Shape errors: \n", "Shape color errors: \n", "Alphanumeric errors: \n", "Letter color errors: \n"]
        out_str = ""
        for i in range(0, len(out_strs)):
            for j in range(0, len(self.wrong_scores[i])):
                out_strs[i] += str(self.wrong_scores[i][j]) + "\n"
            out_str += out_strs[i] + "\n"
        return out_str


    def get_num_crashes(self):
        return self.num_crashes
