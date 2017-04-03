import ImgProcessingCLI.NoiseReduction
import ImgProcessingCLI.NoiseReduction.MeanBlur as MeanBlur
import ImgProcessingCLI.ImageOperation.ImageMath as ImageMath#ImageOperation.ImageMath as ImageMath
import matplotlib.pyplot as plot
from PIL import Image, ImageDraw
import numpy
import ImgProcessingCLI.ImageOperation.Scale as Scale
import ImgProcessingCLI.KernelOperations.KernelMath as KernelMath#KernelOperations.KernelMath as KernelMath
import ImgProcessingCLI.ImageOperation.Paste as Paste

class ColorVaryer:
    RESIZE_SIZE = 100
    KERNEL_SIZE = 7
    BLUR_VARIANCE_KERNEL_SIZE = 7
    VARIANCE_KERNEL_SIZE = 5

    def __init__(self, img, image):

        self.img = Scale.get_img_scaled_to_one_bound(img, ColorVaryer.RESIZE_SIZE)
        self.original_size = self.img.size
        self.image = self.img.load()
        self.mean_blur_img = MeanBlur.get_mean_blurred_rgb_img(self.img, self.image, ColorVaryer.KERNEL_SIZE)
        self.mean_blur_image = self.mean_blur_img.load()
        self.img = KernelMath.crop_img_to_kernel_bounds(self.img, self.image, ColorVaryer.KERNEL_SIZE)
        self.mean_blur_img = KernelMath.crop_img_to_kernel_bounds(self.mean_blur_img, self.mean_blur_image, ColorVaryer.KERNEL_SIZE)
        self.image = self.img.load()
        self.mean_blur_image = self.mean_blur_img.load()
        self.mean_subtract_arr = ImageMath.subtract(self.img.size, self.image, self.mean_blur_image)
        self.init_flat_mean_subtract()
        self.init_normalized_arr()
        self.init_mean_sub_pic()
        self.init_probability_distribution()
        self.init_variance_img()
        self.init_connected_components()
        self.init_biggest_connected_component_mask()



    def init_flat_mean_subtract(self):
        self.flat_mean_sub = numpy.zeros(self.img.size)
        for x in range(0, self.flat_mean_sub.shape[0]):
            for y in range(0, self.flat_mean_sub.shape[1]):
                self.flat_mean_sub[x,y] = numpy.linalg.norm(numpy.asarray(self.mean_subtract_arr[x,y]))

    def init_normalized_arr(self):
        self.norm_flat_mean_sub = numpy.copy(self.flat_mean_sub)
        max = float(numpy.amax(self.norm_flat_mean_sub))
        for x in range(0, self.norm_flat_mean_sub.shape[0]):
            for y in range(0, self.norm_flat_mean_sub.shape[1]):
                self.norm_flat_mean_sub[x,y] = self.norm_flat_mean_sub[x,y]/max

    def init_mean_sub_pic(self):
        self.mean_sub_img = Image.fromarray(numpy.transpose(numpy.uint8((1-self.norm_flat_mean_sub) * 255)))

    def init_probability_distribution(self):
        self.prob_distributions = numpy.zeros((255))
        for x in range(0, self.norm_flat_mean_sub.shape[0]):
            for y in range(0, self.norm_flat_mean_sub.shape[1]):
                if(self.norm_flat_mean_sub[x,y] != 1):
                    self.prob_distributions[int(self.norm_flat_mean_sub[x,y]/(1.0/float(self.prob_distributions.shape[0])))] += 1
                else:
                    self.prob_distributions[self.prob_distributions.shape[0]-1] += 1

    def init_variance_img(self):
        mean_mean_blurred_img = MeanBlur.get_mean_blurred_bw_img(self.mean_sub_img, self.mean_sub_img.load(), ColorVaryer.VARIANCE_KERNEL_SIZE)
        mean_mean_blurred_image = mean_mean_blurred_img.load()
        variance_img_arr = numpy.zeros(self.mean_sub_img.size)
        for x in range(0, variance_img_arr.shape[0]):
            for y in range(0, variance_img_arr.shape[1]):
                variance_img_arr[x,y] = (self.mean_sub_img.load()[x,y] - mean_mean_blurred_image[x,y])**2
        max = numpy.amax(variance_img_arr)
        variance_img_arr = variance_img_arr / float(max)
        self.variance_img = Image.fromarray(numpy.transpose((1-variance_img_arr) * 255))
        self.variance_img = KernelMath.crop_img_to_kernel_bounds(self.variance_img, self.variance_img.load(), ColorVaryer.VARIANCE_KERNEL_SIZE)
        blur_variance_img = MeanBlur.get_mean_blurred_bw_img(self.variance_img, self.variance_img.load(), ColorVaryer.BLUR_VARIANCE_KERNEL_SIZE)# GaussianBlur.get_gaussian_filtered_bw_img(self.variance_img, self.variance_img.load(), 7, 3.0)
        blur_variance_img = KernelMath.crop_img_to_kernel_bounds(blur_variance_img, blur_variance_img.load(), ColorVaryer.BLUR_VARIANCE_KERNEL_SIZE)

        unpasted_mask = ImageMath.get_binary_bw_img(blur_variance_img, blur_variance_img.load(), 254)

        self.shape_mask = Image.new('L', self.original_size)
        Paste.paste_img_onto_img(unpasted_mask, self.shape_mask, (int((self.original_size[0] - unpasted_mask.size[0])/2), int((self.original_size[1] - unpasted_mask.size[1])/2)))


    def init_connected_components(self):
        self.connected_components_map = ImageMath.get_bw_connected_components_map(self.shape_mask, self.shape_mask.load())

    def init_biggest_connected_component_mask(self):
        clusters = ImageMath.convert_connected_component_map_into_clusters(self.connected_components_map)
        biggest_index = 0
        for i in range(1, len(clusters)):
            if len(clusters[i]) > len(clusters[biggest_index]):
                biggest_index = i

        self.big_component_mask = ImageMath.get_connected_component_mask(self.shape_mask.size, clusters[biggest_index])

    def get_shape_mask(self, rescale_dim = None):
        if rescale_dim == None:
            return self.shape_mask
        return self.shape_mask.resize(rescale_dim)

    def get_biggest_component_mask(self, rescale_dim = None):
        if rescale_dim == None:
            return self.big_component_mask
        return self.big_component_mask.resize(rescale_dim)

    '''testing functions'''
    def get_img_filled_at_delta_under_thresh(self, threshold):
        img = Image.new('L', self.norm_flat_mean_sub.shape, 0)
        image = img.load()
        for x in range(0, img.size[0]):
            for y in range(0, img.size[1]):
                if self.norm_flat_mean_sub[x,y] < threshold:
                    image[x,y] = 255
        return img
