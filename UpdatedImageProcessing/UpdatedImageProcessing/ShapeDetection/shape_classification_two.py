from UpdatedImageProcessing.ShapeDetection import utils
from settings import ShapeDetectionSettings

from PIL import Image
import cv2
import os
import numpy

class ShapeClassificationTwo(object):
    def __init__(self, path_to_cropped_img_in):
        self.shape_choices = ShapeDetectionSettings.SHAPE_CHOICES
        self.load_target(path_to_cropped_img_in)
        self.determine_shape()

    def load_target(self,path_to_cropped_img_in):
        self.pil_img = Image.open(path_to_cropped_img_in)
        self.canny_img = utils.alpha_trace(self.pil_img)

        target_mask_img = utils.alpha_fill(self.pil_img)
        _,contours,_ = cv2.findContours(target_mask_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        self.target_contour = contours[0]

    def load_shape_comparison(self):
        self.contour_list = []

        for shape in self.shape_choices:
            dataset = os.path.abspath(utils.__file__)[:-12] + "/target_detection_masks/" + shape + "/"

            for filename in os.listdir(dataset):
                if filename.endswith(".png"):
                    shape_mask_img = cv2.imread(os.path.join(dataset, filename),0)

                    shape_mask_img = Image.open(os.path.join(dataset, filename))
                    shape_mask_img = utils.generate_gaussian_noise_by_level(shape_mask_img, 3, shape_mask_img.width)
                    shape_mask_img = numpy.array(shape_mask_img)

                    _,contours,_ = cv2.findContours(shape_mask_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                    shape_contour = contours[0]

                    comparison = cv2.matchShapes(shape_contour, self.target_contour, 1, 0.0)
                    self.contour_list.append((shape, comparison))

        smallest_difference_index = 0
        for i in range(1, len(self.contour_list)):
            if(self.contour_list[i][1] < self.contour_list[smallest_difference_index][1]):
                smallest_difference_index = i

        self.shape_type = self.contour_list[smallest_difference_index][0]


    def load_polar_side_counter(self):
        self.polar_side_counter = utils.PolarSideCounter(self.canny_img)
        self.polar_side_maximums = self.polar_side_counter.get_polar_side_maximums()
        self.num_polar_side_maximums = len(self.polar_side_maximums)
        #self.polar_side_minimums = self.polar_side_counter.get_polar_side_minimums()
        #self.num_polar_side_minimums = len(self.polar_side_counter.get_polar_side_minimums())
        #self.circle_score = self.polar_side_counter.get_circle_score()
        #self.noise_score = self.polar_side_counter.get_noise_score()
        #self.origin = self.polar_side_counter.get_origin()

    def determine_shape(self):
        self.load_shape_comparison()

        """
        if self.shape_type == "octagon":
            self.load_polar_side_counter()
            if self.circle_score >= ShapeDetectionSettings.CIRCLE_SCORE_THRESHOLD:
                self.shape_type = "circle"
        """

        if self.shape_type == "cross":
            self.load_polar_side_counter()
            if self.num_polar_side_maximums < 4:
                self.shape_type = "triangle"

        if self.shape_type == "rectangle":
            self.load_polar_side_counter()
            if self.num_polar_side_maximums < 3:
                self.shape_type = "semicircle"


    def get_shape_type(self):
        return self.shape_type
