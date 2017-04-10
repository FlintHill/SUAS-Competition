from ImgProcessingCLI.Color.ColorVaryer import ColorVaryer
import ImgProcessingCLI.ImageOperation.Mask as Mask
import ImgProcessingCLI.ImageOperation.ImageMath as ImageMath
import ImgProcessingCLI.Color.TargetColorReader as TargetColorReader
import ImgProcessingCLI.NoiseReduction.GaussianBlur as GaussianBlur
from ImgProcessingCLI.EdgeProcessing.SobelEdge import SobelEdge
import ImgProcessingCLI.EdgeProcessing.CannyEdge as CannyEdge
import ImgProcessingCLI.ImageSegmentation.LetterSegmenter as LetterSegmenter
from PIL import Image, ImageOps, ImageDraw
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
import timeit

import random

from EigenFit.DataMine import *
from EigenFit.Load import *
from EigenFit.Vector import *
'''
'''
class TargetTwo(object):
    KMEANS_RUN_TIMES = 10
    TARGET_BW_BLUR_KERNEL_SIZE = 3
    TARGET_BW_BLUR_STD_DEV = 2.0
    CANNY_EDGE_THRESHOLDS = (20, 40)
    KMEANS_SIDE_CONSTRAINT = 35
    PCA_LETTER_DIM = (40,40)
    LETTER_RESIZE_HEIGHT = int(PCA_LETTER_DIM[1]*0.81666666666667)
    ORIENTATION_INDEXES = ["N", "NW", "W", "SW", "S", "SE", "E", "NE"]
    MODE_REDUCTION_KERNEL_SIZE = 7

    '''note a fair margin around the target is required for some of the assumptions this class makes in order for its
    composite algorithms to function'''

    def __init__(self, target_img_in, target_image_in, letter_categorizer_in, orientation_solver_in):
        self.target_img = target_img_in
        self.target_image = target_image_in
        self.letter_categorizer = letter_categorizer_in
        self.orientation_solver = orientation_solver_in
        self.bw_target_img = self.target_img.convert('L')
        self.bw_target_image = self.bw_target_img.load()

        start_time = timeit.default_timer()
        self.init_edge_imgs()
        print("edge imgs init'd in: " + str(timeit.default_timer() - start_time))
        start_time = timeit.default_timer()
        self.init_color_varyer()
        print("color varyer init'd in: " + str(timeit.default_timer() - start_time))
        start_time = timeit.default_timer()
        self.init_shape_color()
        print("shape color init'd in: " + str(timeit.default_timer() - start_time))
        start_time = timeit.default_timer()
        #self.init_letter_color()
        #print("letter color init'd in: " + str(timeit.default_timer() - start_time))
        start_time = timeit.default_timer()
        self.init_target_shape_img()
        print("target shape img init'd in: " + str(timeit.default_timer() - start_time))
        self.re_init_letter_mask()
        start_time = timeit.default_timer()
        self.init_target_shape_edges_img()
        print("target shape edges init'd in: " + str(timeit.default_timer() - start_time))
        start_time = timeit.default_timer()
        self.init_shape_type()
        print("shape type init'd in: " + str(timeit.default_timer() - start_time))
        start_time = timeit.default_timer()
        self.init_target_orientation()
        print("target orientation init'd in: " + str(timeit.default_timer() - start_time))
        start_time = timeit.default_timer()
        self.init_letter()
        print("letter init'd in: " + str(timeit.default_timer() - start_time))


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

        self.letter_segment_mask = NeighborhoodReduction.get_img_with_pixels_to_neighborhood_mode(self.letter_segment_mask, self.letter_segment_mask.load(), TargetTwo.MODE_REDUCTION_KERNEL_SIZE)
        letter_color_img = Mask.get_bmp_masked_img(self.letter_segment_mask, self.letter_segment_mask.load(), self.target_img, self.target_image)

        self.letter_rgb = ImageMath.get_mean_color_excluding_transparent(letter_color_img, letter_color_img.load())
        self.TARGET_CHARACTER_COLOR = TargetColorReader.get_closest_target_color(self.letter_rgb)


    def init_target_shape_img(self):
        target_img_with_letter_removed = self.target_img.copy().convert('RGB')
        target_image_with_letter_removed = target_img_with_letter_removed.load()

        '''letter_segment_mask_image = self.letter_segment_mask.load()

        for x in range(0, target_img_with_letter_removed.size[0]):
            for y in range(0, target_img_with_letter_removed.size[1]):
                if letter_segment_mask_image[x,y] != 0:
                    target_image_with_letter_removed[x,y] = (int(self.shape_rgb[0]), int(self.shape_rgb[1]), int(self.shape_rgb[2]))
        '''
        kmeans_resized_target_img_with_letter_removed = Scale.get_img_scaled_to_one_bound(target_img_with_letter_removed, TargetTwo.KMEANS_SIDE_CONSTRAINT)
        target_background_kmeans = KMeans.init_with_img(kmeans_resized_target_img_with_letter_removed, kmeans_resized_target_img_with_letter_removed.load(), 2, TargetTwo.KMEANS_RUN_TIMES)
        color_clusters = target_background_kmeans.get_cluster_origins_int()
        target_cluster_color = ColorMath.get_closest_color_from_list(color_clusters, self.shape_rgb)

        rounded_target_img = ColorMath.get_img_rounded_to_colors(target_img_with_letter_removed, target_image_with_letter_removed, color_clusters)
        self.background_target_img = NeighborhoodReduction.get_img_with_pixels_to_neighborhood_mode(rounded_target_img, rounded_target_img.load(), 9)

        background_target_image = self.background_target_img.load()
        self.target_mask = Image.new('L', self.target_img.size)

        target_mask_image = self.target_mask.load()
        for x in range(0, self.target_mask.size[0]):
            for y in range(0, self.target_mask.size[1]):
                if background_target_image[x,y] == target_cluster_color:
                    target_mask_image[x,y] = 255


    def re_init_letter_mask(self):
        target_mask_with_margin = Image.new('L', (self.target_mask.size[0]+2, self.target_mask.size[1]+2))
        Paste.paste_img_onto_img(self.target_mask, target_mask_with_margin, offset = (1,1))

        target_mask_connected_components_map = ImageMath.get_bw_connected_components_map(ImageOps.invert(target_mask_with_margin), ImageOps.invert(target_mask_with_margin).load())
        sorted_target_mask_connected_components_clusters = ImageMath.convert_connected_component_map_into_clusters(target_mask_connected_components_map)
        sorted_target_mask_connected_components_clusters = sorted(sorted_target_mask_connected_components_clusters, key = lambda cluster : len(cluster), reverse = True)
        background_mask = ImageMath.get_connected_component_mask(target_mask_with_margin.size, sorted_target_mask_connected_components_clusters[0])
        background_mask = background_mask.crop((1,1,target_mask_with_margin.size[0]-2, target_mask_with_margin.size[1]-2))

        self.target_mask = ImageOps.invert(background_mask)

        reduced_bounds_target_mask = NeighborhoodReduction.get_img_with_pixels_to_neighborhood_mode(self.target_mask, self.target_mask.load(), 9)

        inside_shape_img = Mask.get_bmp_masked_img(reduced_bounds_target_mask, reduced_bounds_target_mask.load(), self.target_img, self.target_image)


        small_inside_shape_img = inside_shape_img.resize((60,60))
        inside_shape_colors = ImageMath.get_colors_in_img_list_excluding_transparent(small_inside_shape_img, small_inside_shape_img.load())

        '''this threshold is chosen because it is half of the distance between the two closest possible classifiable colors (yellow and brown)'''
        dist_threshold = 41.56921938165306

        #possible_letter_colors = []
        sum = [0,0,0]
        num_instances = 0
        for i in range(0, len(inside_shape_colors)):
            if ColorMath.get_dist_between_colors(self.shape_rgb, inside_shape_colors[i]) > dist_threshold:
                for j in range(0, 3):
                    sum[j] += inside_shape_colors[i][j]
                num_instances += 1

        if num_instances != 0:
            for i in range(0, 3):

                sum[i] = int(float(sum[i])/float(num_instances))
        sum = tuple(sum)
        mean_possible_letter_color = sum
        print("mean possible letter color is: ", mean_possible_letter_color)

        inside_shape_kmeans_colors = [(int(self.shape_rgb[0]), int(self.shape_rgb[1]), int(self.shape_rgb[2])), mean_possible_letter_color]
        letter_shape_img = ColorMath.get_img_rounded_to_colors(self.target_img, self.target_image, inside_shape_kmeans_colors)
        letter_shape_img = Mask.get_bmp_masked_img(reduced_bounds_target_mask, reduced_bounds_target_mask.load(), letter_shape_img, letter_shape_img.load())

        letter_shape_image = letter_shape_img.load()
        shape_cluster_color = ColorMath.get_closest_color_from_list(inside_shape_kmeans_colors, self.shape_rgb)

        new_letter_mask = Image.new('L', self.target_img.size)
        new_letter_mask_image = new_letter_mask.load()


        for x in range(0, letter_shape_img.size[0]):
            for y in range(0, letter_shape_img.size[1]):
                if letter_shape_image[x,y][3] != 0:
                    if letter_shape_image[x,y][0:3] != shape_cluster_color:
                        new_letter_mask_image[x,y] = 255

        new_letter_mask_connected_components_map = ImageMath.get_bw_connected_components_map(new_letter_mask, new_letter_mask_image)
        new_letter_mask_connected_components_clusters = ImageMath.convert_connected_component_map_into_clusters(new_letter_mask_connected_components_map)
        new_letter_mask_connected_components_clusters = sorted(new_letter_mask_connected_components_clusters, key = lambda cluster : len(cluster), reverse = True)
        new_letter_mask = ImageMath.get_connected_component_mask(new_letter_mask.size, new_letter_mask_connected_components_clusters[0])

        '''very similar colors are rounded out after kmeans. If the two kmeans colors are too close, instead round the image to the shape
        color, and the second closest possible color to the list to the shape color'''
        self.letter_segment_mask = new_letter_mask


        #smaller_letter_segment_mask = NeighborhoodReduction.get_img_with_pixels_to_neighborhood_mode(self.letter_segment_mask, self.letter_segment_mask.load(), 7)



        letter_color_img = Mask.get_bmp_masked_img(self.letter_segment_mask, self.letter_segment_mask.load(), self.target_img, self.target_image)
        '''find a way to make sure that neighborhood reduction kernel size will never completely wipe out a letter.
        (or pare it down so much that there are very few color samples left)
        This is at risk of happening with letters that have small stroke width.'''
        letter_color_img2 = letter_color_img
        letter_color_img2 = NeighborhoodReduction.get_img_with_pixels_to_neighborhood_mode(letter_color_img, letter_color_img.load(), 5)

        '''new idea for letter color segmentation:
        use the same method as before where colors with distances above the shape color
        are noted and later averaged to an rgb value, but do it multiple times, and
        set the threhsold to half the distance between the estimated mean letter color
        and the shape color. Should weed out bad instances independent of one color pair?
        (i.e. white to black is harsh so the threshold is easily exceeded)'''

        self.letter_rgb = ImageMath.get_mean_color_excluding_transparent(letter_color_img2, letter_color_img2.load(), percent_outliers = .5)

        self.TARGET_CHARACTER_COLOR = TargetColorReader.get_closest_target_color(self.letter_rgb)





        '''connected components reduction may be needed to remove small noise from letter at this point'''



        '''
        inside_shape_img = Mask.get_bmp_masked_img(self.target_mask, self.target_mask.load(), self.target_img, self.target_image).resize((40,40))
        inside_shape_image = inside_shape_img.load()

        color_vectors = []
        for x in range(0, inside_shape_img.size[0]):
            for y in range(0, inside_shape_img.size[1]):
                if inside_shape_image[x,y][3] != 0:
                    color_vectors.append(inside_shape_image[x,y][0:3])
        shape_letter_kmeans = KMeans(color_vectors, 2, 30, step = 1)
        clusters = shape_letter_kmeans.get_cluster_origins_int()
        letter_shape_img = ColorMath.get_img_rounded_to_colors(self.target_img, self.target_image, clusters).convert('RGBA')



        letter_shape_image = letter_shape_img.load()
        target_mask_image = self.target_mask.load()

        for x in range(0, letter_shape_img.size[0]):
            for y in range(0, letter_shape_img.size[1]):
                if target_mask_image[x,y] == 0:
                    letter_shape_image[x,y] = (0, 0, 0, 0)
        shape_color_cluster = ColorMath.get_closest_color_from_list(clusters, self.shape_rgb)
        new_target_mask = Image.new('L', self.target_mask.size)

        target_mask_image = new_target_mask.load()

        letter_mask = Image.new('L', self.target_mask.size)
        letter_mask_image = letter_mask.load()

        for x in range(0, self.target_mask.size[0]):
            for y in range(0, self.target_mask.size[1]):
                if letter_shape_image[x,y][0:3] == shape_color_cluster:
                    target_mask_image[x,y] = 255
                elif letter_shape_image[x,y][0:3] != shape_color_cluster:# and letter_shape_image[x,y][3] != 0:
                    letter_mask_image[x,y] = 255

        connected_components_map = ImageMath.get_bw_connected_components_map(letter_mask, letter_mask.load())
        connected_components_clusters = ImageMath.convert_connected_component_map_into_clusters(connected_components_map)
        letter_connected_component_cluster = sorted(connected_components_clusters, key = lambda cluster : len(cluster))[0]
        letter_mask = ImageMath.get_connected_component_mask(letter_mask.size, letter_connected_component_cluster)


        for x in range(0, self.target_mask.size[0]):
            for y in range(0, self.target_mask.size[1]):
                if letter_mask_image[x,y] != 0:
                    target_mask_image[x,y] = 255

        self.letter_segment_mask = letter_mask
        #smaller_letter_segment_mask = NeighborhoodReduction.get_img_with_pixels_to_neighborhood_mode(self.letter_segment_mask, self.letter_segment_mask.load(), 11)
        letter_color_img = Mask.get_bmp_masked_img(self.letter_segment_mask, self.letter_segment_mask.load(), self.target_img, self.target_image)
        test_letter_color_img = NeighborhoodReduction.get_img_with_pixels_to_neighborhood_mode(letter_color_img, letter_color_img.load(), 5)





        self.letter_rgb = ImageMath.get_mean_color_excluding_transparent(test_letter_color_img, test_letter_color_img.load())
        self.TARGET_CHARACTER_COLOR = TargetColorReader.get_closest_target_color(self.letter_rgb)
        '''




    def init_target_shape_edges_img(self):
        self.target_edges_img = Mask.get_mask_edges(self.background_target_img, self.background_target_img.load())

    def init_shape_type(self):
        self.shape_type = ShapeType(self.background_target_img.convert('L'), self.target_edges_img)
        self.TARGET_SHAPE = self.shape_type.get_shape_type()

    def init_letter_pca(self):
        self.letter_pca = SimplePCA.init_with_monochrome_img(self.letter_segment_mask, self.letter_segment_mask.load())

    def get_letter_img_resized_to_PCA_dims(self, letter_img):
        out_img = Crop.get_bw_img_cropped_to_bounds(letter_img, letter_img.load(), margin=0)
        out_img = out_img.resize(TargetTwo.PCA_LETTER_DIM)
        return out_img

    def init_target_orientation(self):
        orientation_num = self.orientation_solver.get_letter_img_orientation(self.get_letter_img_resized_to_PCA_dims(self.letter_segment_mask))
        self.TARGET_COMPASS_ORIENTATION = TargetTwo.ORIENTATION_INDEXES[orientation_num]




    def init_letter(self):
        '''letters = string.ascii_uppercase
        rotate_amount = -TargetTwo.ORIENTATION_INDEXES.index(self.TARGET_COMPASS_ORIENTATION)*45
        letter_img = self.get_letter_img_resized_to_PCA_dims(self.letter_segment_mask.rotate(rotate_amount, expand = True))
        self.TARGET_CHARACTER = self.letter_categorizer.predict_letter(letter_img)'''
        rotate_amount = -TargetTwo.ORIENTATION_INDEXES.index(self.TARGET_COMPASS_ORIENTATION)*45
        letter_img = self.get_letter_img_resized_to_PCA_dims(self.letter_segment_mask.rotate(rotate_amount, expand = True))
        scores = self.letter_categorizer.get_algorithm_return_smallest_to_large(letter_img, None)
        print("score: " + str(scores[0:5]))
        self.TARGET_CHARACTER = str(scores[0][0])

    def __repr__(self):
        out = ("orientation: " + str(self.TARGET_COMPASS_ORIENTATION) + "\n"
               + "shape: " + str(self.TARGET_SHAPE) + "\n"
               + "background_color: " + str(self.TARGET_SHAPE_COLOR) + "\n"
               + "alphanumeric: " + str(self.TARGET_CHARACTER) + "\n"
               + "alphanumeric_color: " + str(self.TARGET_CHARACTER_COLOR) + "\n")
        return out

    def as_numpy(self):
        return numpy.asarray((self.TARGET_COMPASS_ORIENTATION, self.TARGET_SHAPE, self.TARGET_SHAPE_COLOR, self.TARGET_CHARACTER, self.TARGET_CHARACTER_COLOR))
