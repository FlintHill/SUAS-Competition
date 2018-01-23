from utils import alpha_trace
from utils import init_harris_corners_and_cluster
from utils.polar_side_counter import PolarSideCounter
import collections
from PIL import Image, ImageOps
import cv2
import numpy

from ImgProcessingCLI.ImgStat import SimplePCA #not tested, will be removed
from ImgProcessingCLI.ImgStat import Clusters, Cluster #not tested, will be removed

CIRCLE_SCORE_THRESHOLD = 0.45 #needs to be optomized
SQUARE_RECTANGLE_EIGEN_RATIO_THRESHOLD = 1.5 #not tested
PENTAGON_STAR_CLUSTER_THRESHOLD = 8 #not tested
OCTAGON_CROSS_CLUSTER_THRESHOLD = 10 #not tested

class ShapeClassification(object):


    def __init__(self, path_to_cropped_img_in):
        self.load_images(path_to_cropped_img_in)
        self.load_polar_side_counter()
        self.determine_shape()

    def load_images(self, path_to_cropped_img_in):
        self.pil_img = Image.open(path_to_cropped_img_in)
        self.cv_img = cv2.imread(path_to_cropped_img_in,0) #loaded in greyscale
        self.monochrome_pil_img = Image.fromarray(self.cv_img)
        #self.canny_img = ImageOps.invert(alpha_trace(path_to_cropped_img_in))
        self.canny_img = alpha_trace(path_to_cropped_img_in)

    def load_polar_side_counter(self):
        self.polar_side_counter = PolarSideCounter(self.canny_img)
        self.num_polar_side_maximums = self.polar_side_counter.get_polar_side_maximums()
        self.num_polar_side_minimums = 0
        self.circle_score = self.polar_side_counter.get_circle_score()
        self.origen = self.polar_side_counter.get_origin()

    def determine_shape(self):
        if self.circle_score >= CIRCLE_SCORE_THRESHOLD:
            self.shape_type = "Circle"
            """elif hough_vote_is_quartercircle(highest_vote_and_radius):
                shape_type = "Quarter-Circle"
            """
        elif self.num_polar_side_maximums == 2:
            self.shape_type = "Semi-Circle"
        elif self.num_polar_side_maximums == 3:
            self.shape_type = "Triangle"
        elif self.num_polar_side_maximums == 6:
            self.shape_type = "Hexagon"
        elif self.num_polar_side_maximums == 7:
            self.shape_type = "Heptagon"
        else:
            if self.num_polar_side_maximums == 4:
                #simplePCA
                pca = SimplePCA.init_with_monochrome_img(self.monochrome_pil_img, self.monochrome_pil_img.load())
                eigenvalues = pca.get_eigenvalues()
                eigen_ratio = abs(eigenvalues[0]/eigenvalues[1])

                if eigen_ratio < 1:
                    eigen_ratio = 1.0/eigen_ratio

                if eigen_ratio > SQUARE_RECTANGLE_EIGEN_RATIO_THRESHOLD:
                    self.shape_type = "Rectangle"
                else:
                    self.shape_type = "Square"
            else:
                num_harris_clusters = init_harris_corners_and_cluster(self.monochrome_pil_img, self.polar_side_maximums, self.polar_side_minimums, self.origen)

                if self.num_polar_side_maximums == 5:
                    if num_harris_clusters < PENTAGON_STAR_CLUSTER_THRESHOLD:
                        self.shape_type = "Pentagon"
                    else:
                        self.shape_type = "Star"
                elif self.num_polar_side_maximums == 8:
                    if num_harris_clusters < OCTAGON_CROSS_CLUSTER_THRESHOLD:
                        self.shape_type = "Octagon"
                    else:
                        self.shape_type = "Cross"
                else:
                    self.shape_type = "Unknown"

    def get_shape_type(self):
        return self.shape_type
