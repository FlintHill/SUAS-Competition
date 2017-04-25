from ImgProcessingCLI.Runtime.TargetCrop import TargetCrop
import numpy
import cv2
import ImgProcessingCLI.ImageOperation.Scale as Scale
from PIL import Image
import ImgProcessingCLI.ImageOperation.ImageMath as ImageMath
import ImgProcessingCLI.TargetTrait.FalseCropCatcher as FalseCropCatcher
from math import sqrt
import ImgProcessingCLI.ImageOperation.Crop as Crop
from ImgProcessingCLI.Geometry.Rectangle import Rectangle

DOWNSCALE_CONSTRAINT = 800
VARIANCE_THRESHOLD = 2000
MAX_SQUARE_CROP_BOUNDS = 200*sqrt(2)

def get_target_crops_from_img(img, geo_stamps, ppsi):
    '''takes the full image, geostamps, and ppsi and finds the targets,
    crops them, and instantiates a list of TargetCrop objects and returns them'''

    '''notes: ppsi of the image should be used in picking a reasonable max crop size'''
    img_downsized = Scale.get_img_scaled_to_one_bound(img, DOWNSCALE_CONSTRAINT).convert('RGB')

    #img.show()
    #img = Image.fromarray(cv2.GaussianBlur(numpy.array(img), (5,5), 3))
    #img = Image.fromarray(cv2.GaussianBlur(numpy.array(img), (7,7), 2))
    #img = img.resize((img.size[0]//5, img.size[1]//5))
    img_downsized = Image.fromarray(cv2.bilateralFilter(numpy.array(img_downsized), 15, 40, 40))
    #img_downsized.show()
    img_downsized.show()
    #img.show()
    image = numpy.array(img_downsized)


    kernel_size = 3
    kernel_margin = (kernel_size - 1)//2
    variance_map = numpy.zeros(img.size)
    '''
    def get_var_in_kernel(image1, xy, kernel_size):
        kernel_margin = (kernel_size-1)//2
        colors = []
        for x in range(xy[0]-kernel_margin, xy[0]+kernel_margin):
            for y in range(xy[1]-kernel_margin, xy[1]+kernel_margin):
                colors.append(image1[x,y])
        colors = numpy.asarray(colors)
        #print("colors: ", colors)
        return numpy.linalg.norm(numpy.var(colors, axis = 1))

    var_img = numpy.zeros((image.shape[0], image.shape[1]))
    for x in range(kernel_margin, image.shape[0]-kernel_margin):
        for y in range(kernel_margin, image.shape[1]-kernel_margin):
            var_img[x,y] = get_var_in_kernel(image, (x,y), kernel_size)
        print("at x: ", x)
    '''

    var_img = numpy.zeros((image.shape[0], image.shape[1]))
    for x in range(kernel_margin, var_img.shape[0]-kernel_margin):
        for y in range(kernel_margin, var_img.shape[1]-kernel_margin):
            sub_arr = image[x-kernel_margin:x+kernel_margin+1, y-kernel_margin:y+kernel_margin+1]

            #print("sub arr shape: ", sub_arr.shape)
            mean, std_dev = (cv2.meanStdDev(sub_arr))
            #print("std dev: ", std_dev)
            '''for some reason porting to this hasn't been the same as it functioned before'''
            var_img[x,y] = numpy.linalg.norm(std_dev)**2
    Image.fromarray(255*var_img/numpy.amax(var_img)).show()
    #pil_var_img = Image.fromarray(255*var_img/numpy.amax(var_img))
    #pil_var_img.show()
    #threshold_img = ImageMath.get_binary_bw_img(pil_var_img, pil_var_img.load(), 40)
    #threshold_img.show()
    var_img = var_img.T
    threshold_img = Image.new('L', (var_img.shape[0], var_img.shape[1]))
    threshold_image = threshold_img.load()

    for x in range(0, threshold_img.size[0]):
        for y in range(0, threshold_img.size[1]):
            if var_img[x,y] > VARIANCE_THRESHOLD:
                threshold_image[x,y] = 255
    threshold_img.show()

    threshold_connected_components_map = ImageMath.get_bw_connected_components_map(threshold_img, threshold_img.load())
    threshold_connected_components = ImageMath.convert_connected_component_map_into_clusters(threshold_connected_components_map)
    resize_ratio = float(img.size[0])/float(img_downsized.size[0])
    min_crop_size = (int((1.0/resize_ratio) * MAX_SQUARE_CROP_BOUNDS), int((1.0/resize_ratio) * MAX_SQUARE_CROP_BOUNDS))
    min_cluster_size = 38
    max_cluster_size = 200

    crops = []
    for i in range(0, len(threshold_connected_components)):
        if len(threshold_connected_components[i]) > min_cluster_size:
            crop_img = ImageMath.get_connected_component_mask(threshold_img.size, threshold_connected_components[i])
            crops.append(crop_img)


    color_crops = []
    crop_margin = 5
    for i in range(0, len(crops)):



        crop_img = crops[i]
        #crop_img.show()
        crop_img_mean_pixel = ImageMath.get_bw_img_mean_pixel(crop_img, crop_img.load())
        #crop_img.show()

        bilat_crop_img = img_downsized.crop((crop_img_mean_pixel[0]-(100 * (1.0/resize_ratio)), crop_img_mean_pixel[1]-(100 * (1.0/resize_ratio)), crop_img_mean_pixel[0]+(100 * (1.0/resize_ratio)), crop_img_mean_pixel[1]+ (100 * (1.0/resize_ratio)))).convert('L')
        bilat_crop_canny_img = Image.fromarray(cv2.Canny(numpy.array(bilat_crop_img), 40, 80))

        #bilat_crop_canny_img.show()

        bilat_start_x = crop_img_mean_pixel[0]-(100 * (1.0/resize_ratio))
        bilat_start_y = crop_img_mean_pixel[1]-(100 * (1.0/resize_ratio))
        bilat_bounding_rect = Crop.get_bw_img_bounds(bilat_crop_canny_img, bilat_crop_canny_img.load())
        #bounding_rect = Rectangle(bilat_start_x + bilat_bounding_rect.get_x(), bilat_start_y + bilat_bounding_rect.get_y(), bilat_bounding_rect.get_width(), bilat_bounding_rect.get_height())
        #print("bounding rect: ", bounding_rect)
        bounding_rect = Crop.get_bw_img_bounds(crop_img, crop_img.load())
        bounding_rect.set_x(int(bounding_rect.get_x() * resize_ratio) - crop_margin)
        bounding_rect.set_y(int(bounding_rect.get_y() * resize_ratio) - crop_margin)
        bounding_rect.set_width(int(bounding_rect.get_width() * resize_ratio) + 3*crop_margin)
        bounding_rect.set_height(int(bounding_rect.get_height() * resize_ratio) + 3*crop_margin)
        append_img = Crop.get_img_cropped_to_bounds(img, bounding_rect)

        color_crops.append((numpy.asarray(crop_img_mean_pixel), append_img))

    '''kills crops in the same list whose center are very close to each other (sometimes the same target pops up twice)'''
    min_dist_threshold = 15

    min_area = 1600
    max_area = 48400
    i = 0
    while i < len(color_crops):
        sorted_crops = sorted(color_crops, key = lambda crop : numpy.linalg.norm(crop[0]-color_crops[i][0]))
        '''sorted_crops[1][0] so that it excludes a measurement to itself'''
        if numpy.linalg.norm(sorted_crops[1][0] - color_crops[i][0]) < min_dist_threshold:
            if not (color_crops[i][1].size[0]*color_crops[i][1].size[1] > sorted_crops[1][1].size[0]*sorted_crops[1][1].size[1]):
                del color_crops[i]
            else:
                i+=1
        else:

            i+=1

    i = 0
    while i < len(color_crops):
        area = color_crops[i][1].size[0]*color_crops[i][1].size[1]
        if area < min_area or area > max_area:
            del color_crops[i]
        else:
            i += 1

    i = 0
    KMEANS_RUN_TIMES = 10
    MIN_TOTAL_CLUSTER_DISTANCE_SUM = 370
    while i < len(color_crops):
        #print('color crops[i][1]: ', color_crops[i][1])
        colors = numpy.array(color_crops[i][1].convert('RGB')).reshape((-1, 3))
        colors = numpy.float32(colors)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, KMEANS_RUN_TIMES, 1.0)
        ret, labels, color_clusters = cv2.kmeans(colors, 3, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        #print("color clusters: ", color_clusters)
        dist_sum = 0
        dist_sum += numpy.linalg.norm(color_clusters[1]-color_clusters[0])
        dist_sum += numpy.linalg.norm(color_clusters[2]-color_clusters[1])
        dist_sum += numpy.linalg.norm(color_clusters[0]-color_clusters[2])
        print("dist sum is: ", dist_sum)
        if not dist_sum > MIN_TOTAL_CLUSTER_DISTANCE_SUM:
            del color_crops[i]
        else:
            i += 1



    target_crops = []



    for i in range(0, len(color_crops)):
        target_crops.append(TargetCrop(img, color_crops[i][1], geo_stamps, color_crops[i][0], ppsi))
    return target_crops
