from ImgStat.KMeans import KMeans
from Color.ColorSplitter import ColorSplitter
import NoiseReduction.GaussianBlur as GaussianBlur
from EdgeProcessing.SobelEdge import SobelEdge
import EdgeProcessing.CannyEdge as CannyEdge
from Geometry.PolarSideCounter import PolarSideCounter
import Color.TargetColorReader as TargetColorReader
from ImgStat.SimplePCA import SimplePCA
from TargetTrait.TargetDirection import TargetDirection
from PIL import ImageDraw

class Target:
    BLUR_SHAPE_KERNELSIZE = 3
    BLUR_SHAPE_STD_DEV = 2
    CANNY_SHAPE_THRESHOLDS = (20, 40)
    CANNY_TOTAL_THRESHOLDS = (20, 40)
    BLUR_TOTAL_KERNELSIZE = 5
    BLUR_TOTAL_STD_DEV = 5
    def __init__(self, img_in, image_in):
        self.img = img_in
        self.image = image_in
        self.init_edge_imgs()
        self.color_splitter = ColorSplitter.init_with_kmeans(self.img, self.image, 3, 20, 3)
        self.color_splitter.sort_by_area()
        self.unfilled_color_layers = self.color_splitter.get_color_layers().clone()
        self.color_splitter.sort_by_area_then_fill_gaps()
        self.color_layers = self.color_splitter.get_color_layers()
        self.shape_layer = self.get_shape_color_layer()
        
        self.unfilled_background_layer = self.unfilled_color_layers[len(self.unfilled_color_layers) - 1]
        #self.unfilled_background_layer.get_layer_img().show()
        self.init_side_count()
        self.init_shape_color()
        self.init_shape_PCA()
        self.init_target_direction()
        self.init_letter_layer()
        self.init_letter_color()
      
    def init_edge_imgs(self):
        self.bw_img = self.img.copy().convert('L')
        self.gaussian_img = GaussianBlur.get_gaussian_filtered_bw_img(self.bw_img, self.bw_img.load(), Target.BLUR_TOTAL_KERNELSIZE, Target.BLUR_TOTAL_STD_DEV)
        self.sobel_edge = SobelEdge(self.gaussian_img)
        self.canny_img = CannyEdge.get_canny_img(self.sobel_edge, Target.CANNY_TOTAL_THRESHOLDS)
        #self.canny_img.show()
        
    def init_side_count(self):
        shape_img = self.shape_layer.get_layer_img().copy()
        shape_image = shape_img.load()
        shape_img = GaussianBlur.get_gaussian_filtered_bw_img(shape_img, shape_image, Target.BLUR_SHAPE_KERNELSIZE, Target.BLUR_SHAPE_STD_DEV)
        shape_image = shape_img.load()
        self.shape_sobel = SobelEdge(shape_img)
        self.shape_canny_img = CannyEdge.get_canny_img(self.shape_sobel, Target.CANNY_SHAPE_THRESHOLDS)
        self.polar_side_counter = PolarSideCounter(self.shape_canny_img, self.shape_canny_img.load())
        #self.polar_side_counter.get_maximums_drawn_to_img().show()
    
    def init_shape_color(self):
        self.shape_color = TargetColorReader.get_closest_target_color(self.shape_layer.get_color())
        print("shape color: " + str(self.shape_color))
    
    '''assuming the color splitter is sorted by top to bottom layer, the layer with the shape should always be
    2nd from the end, because it is directly after the background'''
    def get_shape_color_layer(self):
        return self.color_layers[len(self.color_layers)-2]
    
    def init_shape_PCA(self):
        '''to improve, remove the background color from the image then do canny on only the shape and letter.
        Will eliminate noise from background. Worth noting that the noise from background probably matters very
        little in the calculation'''
        self.pca = SimplePCA.init_with_canny_img(self.canny_img, self.canny_img.load())
     
    def init_target_direction(self):
        self.target_direction = TargetDirection(self.pca.get_eigenvectors(), self.polar_side_counter)
        
    def init_letter_layer(self):
        self.letter_layer = self.color_layers[0]
        #self.letter_layer.get_layer_img().show()
        self.remove_possible_false_border_around_letter()
    
    def remove_possible_false_border_around_letter(self):
        '''by appending the letter layer, which may have an incorrect border around it as a result of KMeans,
        onto the background layer, the false border will connect with the background layer. As a result, 
        flood-filling any place that is the background and not the letter will remove the entire background
        from the appended letter-to-background image'''
        background_and_letter_layer = self.unfilled_background_layer.get_layer_filled_with_layer(self.letter_layer)
        '''chose (0,0) as a start because that seemed guaranteed to have the background in it. However,
        I can see times where this is not the case, and it may be necessary to add a method to ColorLayer
        that will return a pixel (doesn't really matter which) that is a part of the color layer, and 
        the flood-filling will begin there'''
        ImageDraw.floodfill(background_and_letter_layer.get_layer_img(), (0,0), 0)
        self.letter_layer = background_and_letter_layer
        self.letter_layer.get_layer_img().show()
        #background_and_letter_layer.get_layer_img().show()
    
    def init_letter_color(self):
        self.letter_color = TargetColorReader.get_closest_target_color(self.letter_layer.get_color())
        print("letter color: " + str(self.letter_color))