from Stat.KMeans import KMeans
from Color.ColorSplitter import ColorSplitter
import NoiseReduction.GaussianBlur as GaussianBlur
from EdgeProcessing.SobelEdge import SobelEdge
import EdgeProcessing.CannyEdge as CannyEdge
from Geometry.PolarSideCounter import PolarSideCounter
import Color.TargetColorReader as TargetColorReader
from Stat.SimplePCA import SimplePCA

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
        self.color_splitter.sort_by_area_then_fill_gaps()
        self.color_layers = self.color_splitter.get_color_layers()
        self.shape_layer = self.get_shape_color_layer()
        self.init_side_count()
        self.init_shape_color()
        self.init_shape_PCA()
      
    def init_edge_imgs(self):
        self.bw_img = self.img.copy().convert('L')
        self.gaussian_img = GaussianBlur.get_gaussian_filtered_bw_img(self.bw_img, self.bw_img.load(), Target.BLUR_TOTAL_KERNELSIZE, Target.BLUR_TOTAL_STD_DEV)
        self.sobel_edge = SobelEdge(self.gaussian_img)
        self.canny_img = CannyEdge.get_canny_img(self.sobel_edge, Target.CANNY_TOTAL_THRESHOLDS)
        self.canny_img.show()
        
    def init_side_count(self):
        shape_img = self.shape_layer.get_layer_img().copy()
        shape_image = shape_img.load()
        shape_img = GaussianBlur.get_gaussian_filtered_bw_img(shape_img, shape_image, Target.BLUR_SHAPE_KERNELSIZE, Target.BLUR_SHAPE_STD_DEV)
        shape_image = shape_img.load()
        self.shape_sobel = SobelEdge(shape_img)
        self.shape_canny_img = CannyEdge.get_canny_img(self.shape_sobel, Target.CANNY_SHAPE_THRESHOLDS)
        self.polar_side_counter = PolarSideCounter(self.shape_canny_img, self.shape_canny_img.load())
        self.polar_side_counter.get_maximums_drawn_to_img().show()
    
    def init_shape_color(self):
        self.shape_color = TargetColorReader.get_closest_target_color(self.shape_layer.get_color())
    
    '''assuming the color splitter is sorted by top to bottom layer, the layer with the shape should always be
    2nd from the end, because it is directly after the background'''
    def get_shape_color_layer(self):
        return self.color_layers[len(self.color_layers)-2]
    
    def init_shape_PCA(self):
        self.pca = SimplePCA.init_with_canny_img(self.canny_img, self.canny_img.load())
        print("eigenvectors: " + str(self.pca.get_eigenvectors()))
        