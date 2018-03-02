from settings import ShapeDetectionSettings
from utils import alpha_trace
from utils import init_harris_corners_and_cluster
from utils.polar_side_counter import PolarSideCounter
from utils.simple_pca import SimplePCA
from utils.hough_lines import HoughSideCounter
from PIL import Image
import cv2
import random

class ShapeClassification(object):
    def __init__(self, path_to_cropped_img_in):
        self.load_images(path_to_cropped_img_in)
        self.load_polar_side_counter()
        self.determine_shape()

    def load_images(self, path_to_cropped_img_in):
        self.pil_img = Image.open(path_to_cropped_img_in)
        self.cv_img = cv2.imread(path_to_cropped_img_in)
        self.monochrome_pil_img = Image.fromarray(cv2.imread(path_to_cropped_img_in,0))
        self.canny_img = alpha_trace(path_to_cropped_img_in)

    def load_polar_side_counter(self):
        self.polar_side_counter = PolarSideCounter(self.canny_img)
        self.polar_side_maximums = self.polar_side_counter.get_polar_side_maximums()
        self.num_polar_side_maximums = len(self.polar_side_maximums)
        self.polar_side_minimums = self.polar_side_counter.get_polar_side_minimums()
        self.num_polar_side_minimums = len(self.polar_side_counter.get_polar_side_minimums())
        self.circle_score = self.polar_side_counter.get_circle_score()
        self.noise_score = self.polar_side_counter.get_noise_score()
        self.origin = self.polar_side_counter.get_origin()

    def determine_shape(self):
        if self.circle_score >= ShapeDetectionSettings.CIRCLE_SCORE_THRESHOLD:
            self.shape_type = "circle"
        elif self.noise_score >= ShapeDetectionSettings.NOISE_SCORE_THRESHOLD:
            self.shape_type = "NOISE"
        elif len(HoughSideCounter(self.cv_img, self.canny_img, ShapeDetectionSettings.QUARTER_CIRCLE_HOUGH_THRESHOLD).get_sides()) == 2:
            self.shape_type = "quarter_circle"
        elif self.num_polar_side_maximums not in range(2,8):
            #panic -- chose random shape
            self.shape_type = random.choice(ShapeDetectionSettings.SHAPE_CHOICES)
        elif self.num_polar_side_maximums == 2:
            self.shape_type = "semicircle"
        elif self.num_polar_side_maximums == 3:
            self.shape_type = "triangle"
        elif self.num_polar_side_maximums == 6:
            self.shape_type = "hexagon"
        elif self.num_polar_side_maximums == 7:
            self.shape_type = "heptagon"
        else:
            if self.num_polar_side_maximums == 4:
                #self.shape_type = "trapezoid"
                pca = SimplePCA.init_with_monochrome_img(self.monochrome_pil_img)
                eigenvalues = pca.get_eigenvalues()
                eigen_ratio = abs(eigenvalues[0]/eigenvalues[1])

                if eigen_ratio < 1:
                    eigen_ratio = 1.0/eigen_ratio

                if eigen_ratio > ShapeDetectionSettings.SQUARE_RECTANGLE_EIGEN_RATIO_THRESHOLD:
                    self.shape_type = "rectangle"
                else:
                    self.shape_type = "square"

            else:
                num_harris_clusters = init_harris_corners_and_cluster(self.monochrome_pil_img, self.polar_side_maximums, self.polar_side_minimums, self.origin)

                if self.num_polar_side_maximums == 5:
                    if num_harris_clusters < ShapeDetectionSettings.PENTAGON_STAR_CLUSTER_THRESHOLD:
                        self.shape_type = "pentagon"
                    else:
                        self.shape_type = "star"
                elif self.num_polar_side_maximums == 8:
                    if num_harris_clusters < ShapeDetectionSettings.OCTAGON_CROSS_CLUSTER_THRESHOLD:
                        self.shape_type = "octagon"
                    else:
                        self.shape_type = "cross"

    def get_shape_type(self):
        return self.shape_type
