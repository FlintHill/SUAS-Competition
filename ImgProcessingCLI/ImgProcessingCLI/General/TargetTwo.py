from ImgProcessingCLI.Color.ColorVaryer import ColorVaryer
import ImgProcessingCLI.ImageOperation.Mask as Mask
import ImgProcessingCLI.ImageOperation.ImageMath as ImageMath
import ImgProcessingCLI.Color.TargetColorReader as TargetColorReader
import ImgProcessingCLI.NoiseReduction.GaussianBlur as GaussianBlur
from ImgProcessingCLI.EdgeProcessing.SobelEdge import SobelEdge
import ImgProcessingCLI.EdgeProcessing.CannyEdge as CannyEdge
import ImgProcessingCLI.ImageSegmentation.LetterSegmenter as LetterSegmenter
from PIL import Image, ImageOps
from ImgProcessingCLI.ImgStat.KMeans import KMeans
import ImgProcessingCLI.Color.ColorMath as ColorMath
import ImgProcessingCLI.ImageOperation.Scale as Scale
import ImgProcessingCLI.NoiseReduction.NeighborhoodReduction as NeighborhoodReduction
from ImgProcessingCLI.TargetTrait.ShapeType import ShapeType
from ImgProcessingCLI.TargetTrait.TargetDirection import TargetDirection
from ImgProcessingCLI.ImgStat.SimplePCA import SimplePCA
import ImgProcessingCLI.ImageOperation.Crop as Crop
import ImgProcessingCLI.ImageOperation.Paste as Paste
import numpy
import string
from sklearn import ensemble
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB

import random

from EigenFit.DataMine import *
from EigenFit.Load import *
from EigenFit.Vector import *
'''
'''
class TargetTwo(object):
    KMEANS_RUN_TIMES = 5
    TARGET_BW_BLUR_KERNEL_SIZE = 3
    TARGET_BW_BLUR_STD_DEV = 2.0
    CANNY_EDGE_THRESHOLDS = (20, 40)
    KMEANS_SIDE_CONSTRAINT = 35
    PCA_LETTER_DIM = (40,40)
    LETTER_RESIZE_HEIGHT = int(PCA_LETTER_DIM[1]*0.81666666666667)
    ORIENTATION_INDEXES = ["N", "NW", "W", "SW", "S", "SE", "E", "NE"]

    def __init__(self, target_img_in, target_image_in, letter_categorizer_in, orientation_solver_in):
        self.target_img = target_img_in
        self.target_image = target_image_in
        self.letter_categorizer = letter_categorizer_in
        self.orientation_solver = orientation_solver_in
        self.bw_target_img = self.target_img.convert('L')
        self.bw_target_image = self.bw_target_img.load()

        self.init_edge_imgs()
        self.init_color_varyer()
        self.init_shape_color()
        self.init_letter_color()
        self.init_target_shape_img()
        self.init_target_shape_edges_img()
        self.init_shape_type()
        self.init_letter_pca()
        self.init_target_orientation()
        self.init_letter()
        #self.init_possible_letter_orientation_imgs()
        #self.run_possible_letter_orientation_imgs_through_letter_recognition()

    def init_edge_imgs(self):
        self.gaussian_blurred_target_img = GaussianBlur.get_gaussian_filtered_bw_img(self.bw_target_img, self.bw_target_image, TargetTwo.TARGET_BW_BLUR_KERNEL_SIZE, TargetTwo.TARGET_BW_BLUR_STD_DEV)
        self.target_sobel_edge = SobelEdge(self.gaussian_blurred_target_img)
        self.target_canny_edge_img = CannyEdge.get_canny_img(self.target_sobel_edge, TargetTwo.CANNY_EDGE_THRESHOLDS)

    def init_color_varyer(self):
        self.color_varyer = ColorVaryer(self.target_img, self.target_image)

    def init_shape_color(self):
        connected_component_shape_mask = self.color_varyer.get_biggest_component_mask(rescale_dim = self.target_img.size)
        shape_color_img = Mask.get_bmp_masked_img(connected_component_shape_mask, connected_component_shape_mask.load(), self.target_img, self.target_image)

        self.shape_rgb = ImageMath.get_mean_color_excluding_transparent(shape_color_img, shape_color_img.load())
        self.TARGET_SHAPE_COLOR = TargetColorReader.get_closest_target_color(self.shape_rgb)

    def init_letter_color(self):
        shape_mask = self.color_varyer.get_shape_mask(rescale_dim = self.target_img.size)
        shape_mask_edges = Mask.get_mask_edges(shape_mask, shape_mask.load())

        letter_segment_mask_all_components = LetterSegmenter.get_segmented_letter_img(self.target_img.size, shape_mask_edges.load(), self.target_canny_edge_img.load())

        letter_segment_mask_ccomponents_map = ImageMath.get_bw_connected_components_map(letter_segment_mask_all_components, letter_segment_mask_all_components.load())
        letter_segment_mask_clusters = sorted(ImageMath.convert_connected_component_map_into_clusters(letter_segment_mask_ccomponents_map), key = lambda cluster : len(cluster), reverse = True)
        if len(letter_segment_mask_clusters) > 0:
            self.letter_segment_mask = ImageMath.get_connected_component_mask(self.target_img.size, letter_segment_mask_clusters[0])
        else:
            '''need to throw something because the letter mask is empty'''
            self.letter_segment_mask = Image.new('L', self.target_img.size)

        self.letter_segment_mask = NeighborhoodReduction.get_img_with_pixels_to_neighborhood_mode(self.letter_segment_mask, self.letter_segment_mask.load(), 7)

        letter_color_img = Mask.get_bmp_masked_img(self.letter_segment_mask, self.letter_segment_mask.load(), self.target_img, self.target_image)

        self.letter_rgb = ImageMath.get_mean_color_excluding_transparent(letter_color_img, letter_color_img.load())
        self.TARGET_CHARACTER_COLOR = TargetColorReader.get_closest_target_color(self.letter_rgb)


    def init_target_shape_img(self):
        target_img_with_letter_removed = self.target_img.copy().convert('RGB')
        target_image_with_letter_removed = target_img_with_letter_removed.load()

        letter_segment_mask_image = self.letter_segment_mask.load()

        for x in range(0, target_img_with_letter_removed.size[0]):
            for y in range(0, target_img_with_letter_removed.size[1]):
                if letter_segment_mask_image[x,y] != 0:
                    target_image_with_letter_removed[x,y] = (int(self.shape_rgb[0]), int(self.shape_rgb[1]), int(self.shape_rgb[2]))

        kmeans_resized_target_img_with_letter_removed = Scale.get_img_scaled_to_one_bound(target_img_with_letter_removed, TargetTwo.KMEANS_SIDE_CONSTRAINT)
        target_background_kmeans = KMeans.init_with_img(kmeans_resized_target_img_with_letter_removed, kmeans_resized_target_img_with_letter_removed.load(), 2, TargetTwo.KMEANS_RUN_TIMES)
        color_clusters = target_background_kmeans.get_cluster_origins_int()
        rounded_target_img = ColorMath.get_img_rounded_to_colors(target_img_with_letter_removed, target_image_with_letter_removed, color_clusters)
        self.background_target_img = NeighborhoodReduction.get_img_with_pixels_to_neighborhood_mode(rounded_target_img, rounded_target_img.load(), 9)

    def init_target_shape_edges_img(self):
        self.target_edges_img = Mask.get_mask_edges(self.background_target_img, self.background_target_img.load())

    def init_shape_type(self):
        self.shape_type = ShapeType(self.background_target_img.convert('L'), self.target_edges_img)
        self.TARGET_SHAPE = self.shape_type.get_shape_type()

    def init_letter_pca(self):
        self.letter_pca = SimplePCA.init_with_monochrome_img(self.letter_segment_mask, self.letter_segment_mask.load())

    def get_letter_img_resized_to_PCA_dims(self, letter_img):
        out_img = Crop.get_bw_img_cropped_to_bounds(letter_img, letter_img.load())
        out_img = out_img.resize(TargetTwo.PCA_LETTER_DIM)
        return out_img

        '''resized_letter_img = Crop.get_bw_img_cropped_to_bounds(letter_img, letter_img.load(), margin = 1)
        resized_letter_img = Scale.scale_img_to_height(resized_letter_img, TargetTwo.LETTER_RESIZE_HEIGHT)
        base_img = Image.new('L', TargetTwo.PCA_LETTER_DIM, 0)
        offset = ((TargetTwo.PCA_LETTER_DIM[0]//2) - (int(round(resized_letter_img.size[0]/2.0))), (TargetTwo.PCA_LETTER_DIM[1]//2) - (int(round(resized_letter_img.size[1]/2.0))))
        Paste.paste_img_onto_img(resized_letter_img, base_img, offset)
        resized_letter_img = base_img
        return resized_letter_img'''

    def init_target_orientation(self):
        orientation_num = self.orientation_solver.get_letter_img_orientation(self.get_letter_img_resized_to_PCA_dims(self.letter_segment_mask))
        self.TARGET_COMPASS_ORIENTATION = TargetTwo.ORIENTATION_INDEXES[orientation_num]


    def init_letter(self):
        rotate_amount = -TargetTwo.ORIENTATION_INDEXES.index(self.TARGET_COMPASS_ORIENTATION)*45
        letter_img = self.get_letter_img_resized_to_PCA_dims(self.letter_segment_mask.rotate(rotate_amount, expand = True))
        scores = self.letter_categorizer.get_algorithm_return_smallest_to_large(letter_img, None)
        print("score: " + str(scores[0:5]))
        self.TARGET_CHARACTER = scores[0][0]

    '''
    def init_possible_letter_orientation_imgs(self):
        ''''''should not be resized before as when it is rotated the sizing will be off''''''
        letter_img_resized_to_pca_dims = self.get_letter_img_resized_to_PCA_dims(self.letter_segment_mask)


        self.target_direction = TargetDirection(self.letter_pca.get_eigenvectors(), self.letter_pca.get_eigenvalues(), self.shape_type.get_polar_side_counter())
        ''''''where the first index is the img, the second the compass direction, the third the polar angle''''''
        self.possible_letter_orientation_imgs = self.target_direction.get_letter_imgs_rotated_to_possible_directions(letter_img_resized_to_pca_dims)



        for i in range(0, len(self.possible_letter_orientation_imgs)):
            self.possible_letter_orientation_imgs[i] = (self.possible_letter_orientation_imgs[i][0].resize(TargetTwo.PCA_LETTER_DIM), self.possible_letter_orientation_imgs[i][1], self.possible_letter_orientation_imgs[i][2])



    def run_possible_letter_orientation_imgs_through_letter_recognition(self):


        best_fit_character = ""
        best_fit_score = -1
        best_fit_direction = ""

        for i in range(0, len(self.possible_letter_orientation_imgs)):
            if i == 0:
                img_vector = VectorMath.gray_img_to_vector(self.get_letter_img_resized_to_PCA_dims(self.letter_segment_mask))
                projection_weights = EigenProjector.get_projection_weights(img_vector, self.letter_categorizer.get_eigenvectors(), self.letter_categorizer.get_mean())[0:20]
                reconstruction_vector = EigenProjector.get_reconstruction_img_vector(projection_weights, self.letter_categorizer.get_eigenvectors()) + self.letter_categorizer.get_mean()
                #VectorMath.img_vector_to_gray_img(img_vector, img_dimensions).show()
                #VectorMath.img_vector_to_gray_img(reconstruction_vector, TargetTwo.PCA_LETTER_DIM).show()

            iter_scores = self.letter_categorizer.get_algorithm_return_smallest_to_large(self.get_letter_img_resized_to_PCA_dims(self.letter_segment_mask), None)#self.letter_categorizer.get_algorithm_return_smallest_to_large((self.possible_letter_orientation_imgs[i][0]), None)

            print("iter scores: " + str(iter_scores[0:4]))
            iter_letter = iter_scores[0][0]

            iter_score = iter_scores[0][1]
            if iter_score < best_fit_score or best_fit_score < 0:
                best_fit_score = iter_score
                best_fit_character = iter_letter
                best_fit_direction = self.possible_letter_orientation_imgs[i][1]




        self.TARGET_CHARACTER = best_fit_character#str(letters[prediction[0]])
    '''
    def __repr__(self):
        out = ("orientation: " + str(self.TARGET_COMPASS_ORIENTATION) + "\n"
               + "shape: " + str(self.TARGET_SHAPE) + "\n"
               + "background_color: " + str(self.TARGET_SHAPE_COLOR) + "\n"
               + "alphanumeric: " + str(self.TARGET_CHARACTER) + "\n"
               + "alphanumeric_color: " + str(self.TARGET_CHARACTER_COLOR) + "\n")
        return out

    def as_numpy(self):
        return numpy.asarray((self.TARGET_COMPASS_ORIENTATION, self.TARGET_SHAPE, self.TARGET_SHAPE_COLOR, self.TARGET_CHARACTER, self.TARGET_CHARACTER_COLOR))
