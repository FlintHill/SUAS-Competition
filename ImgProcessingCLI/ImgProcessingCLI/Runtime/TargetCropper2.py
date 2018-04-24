from ImgProcessingCLI.Runtime.TargetCrop import TargetCrop
import ImgProcessingCLI.Color.TargetColorReader as TargetColorReader
import ImgProcessingCLI.Color.ColorMath as ColorMath
import numpy
import ImgProcessingCLI.ImageOperation.Scale as Scale
from PIL import Image
import cv2
from math import sqrt
import ImgProcessingCLI.ImageOperation.Crop as Crop
from ImgProcessingCLI.Geometry.Rectangle import Rectangle
import ImgProcessingCLI.TargetTrait.FalseCropCatcher as FalseCropCatcher
import timeit
import scipy
from scipy.ndimage.filters import uniform_filter
from scipy.ndimage.filters import convolve
import ImgProcessingCLI.Color.TargetColorReader as TargetColorReader


DOWNSCALE_CONSTRAINT = 1800#1200#600'''used to be 600 but had issues with accuracy'''
LOCAL_VARIANCE_THRESHOLD = 600#1000'''is 1000 for 400-ish ft altitude'''
LOCAL_VARIANCE_KERNEL_SIZE = 3
LOCAL_VARIANCE_KERNEL_MARGIN = (LOCAL_VARIANCE_KERNEL_SIZE-1)//2
BILAT_FILTER_THRESHOLDS = (15, 40, 40)
MIN_CROP_DIST_AWAY = 120
MIN_MAX_CROP_AREA_INCHES = (300, 14400)
CROP_MARGIN_INCHES = 2#6
MIN_CROP_SIZE_INCHES = 24#36
WIDTH_LENGTH_CUTOFF_RATIO = 3
MEDIAN_BLUR_RUN_TIMES = 4

def get_target_crops_from_img(parent_img, geo_stamps, ppsi, get_centers = False):
    downsized_parent_image = numpy.array(Scale.get_img_scaled_to_one_bound(parent_img, DOWNSCALE_CONSTRAINT).convert('RGB'))

    downscale_multiplier = float(DOWNSCALE_CONSTRAINT)/float(parent_img.size[0])
    upscale_multiplier = 1.0/downscale_multiplier
    img = Image.fromarray(downsized_parent_image)



    downsized_parent_image = cv2.bilateralFilter(downsized_parent_image, BILAT_FILTER_THRESHOLDS[0], BILAT_FILTER_THRESHOLDS[1], BILAT_FILTER_THRESHOLDS[2])
    for i in range(0, MEDIAN_BLUR_RUN_TIMES):
        downsized_parent_image = cv2.medianBlur(downsized_parent_image, 3)

    start_time = timeit.default_timer()




    #var_image = create_local_variance_image(cv2.cvtColor(downsized_parent_image, cv2.COLOR_RGB2GRAY))
    #Image.fromarray(255*var_image/numpy.amax(var_image)).show()
    #print("var image shape: ", var_image.shape)



    print("time elapsed creating var image: ", timeit.default_timer() - start_time)
    start_time = timeit.default_timer()



    gaussian_blurred_downsized_image = cv2.GaussianBlur(downsized_parent_image, (5,5), 3.0)
    thresh_var_img = Image.fromarray(cv2.Canny(gaussian_blurred_downsized_image, 100, 150, apertureSize = 3))#create_thresholded_local_variance_img(var_image)#Image.fromarray(cv2.Canny(gaussian_blurred_downsized_image, 20, 40, apertureSize = 3))
    #thresh_var_img.show()
    print("time elapsed thresholding variance img: ", timeit.default_timer() - start_time)
    downsized_canny_image = numpy.uint8(numpy.array(thresh_var_img))

    contour_image, contours, hierarchy = cv2.findContours(downsized_canny_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    print("contours shape: ", len(contours), ", hierarchy shape: ", hierarchy.shape)

    drawn_contour_image = numpy.array(Image.new('RGB', tuple(contour_image.T.shape)))
    good_contours = []
    for i in range(0, hierarchy.shape[1]):
        if hierarchy[0][i][2] >= 0:# and hierarchy[0][i][0] >= 0:
            good_contours.append(contours[i])

    print("good contours shape: ", len(good_contours))
    drawn_contour_image = cv2.drawContours(drawn_contour_image, good_contours, -1, (0,255,0), 1)

    '''print("hierarchy is: ", hierarchy)
    for i in range(0, hierarchy.shape[0]):
        print("hierarchy [i,0,2] is: ", hierarchy[i][0][2])
        if hierarchy[i][0][2] == -1:
            drawn_contour_image = cv2.drawContours(drawn_contour_image, contours[i], -1, (0,255,0), 3)
    #drawn_contour_image = cv2.drawContours(numpy.array(Image.new('RGB', tuple(contour_image.T.shape))), contours, -1, (0,255,0), 3)'''


    crop_masks = []
    for i in range(0, len(good_contours)):
        iter_contour_image = numpy.zeros((downsized_parent_image.shape[0], downsized_parent_image.shape[1]))
        iter_contour_image = cv2.drawContours(iter_contour_image, good_contours, i, 255, 3)
        iter_contour_img = Image.fromarray(iter_contour_image)
        crop_masks.append(iter_contour_img)

    color_target_rects = []
    pixel_crop_margin = int(float(CROP_MARGIN_INCHES) * sqrt(ppsi))+1
    for i in range(0, len(crop_masks)):
        mask_bounding_rect = Crop.get_bw_img_bounds(crop_masks[i], crop_masks[i].load())
        '''for some reason adding a crop margin to the right and bottom edge to the crop requires more than just
        2* the crop margin. The *3 is to mitigate this, and seems to work'''
        parent_img_bounding_rect = Rectangle(int(upscale_multiplier * mask_bounding_rect.get_x()) - pixel_crop_margin, int(upscale_multiplier * mask_bounding_rect.get_y()) - pixel_crop_margin, int(upscale_multiplier * mask_bounding_rect.get_width()) + (2 * pixel_crop_margin), int(upscale_multiplier * mask_bounding_rect.get_height()) + (2 * pixel_crop_margin))
        crop_midpoint = parent_img_bounding_rect.get_center()
        color_target_rects.append((crop_midpoint, parent_img_bounding_rect))

    print("len before first remove step: ", len(color_target_rects))
    remove_duplicate_imgs_by_proximity(color_target_rects, ppsi)
    print("len before second remove step: ", len(color_target_rects))
    remove_crops_by_area(color_target_rects, ppsi)

    color_target_crops = []
    for i in range(0, len(color_target_rects)):
        color_target_crops.append((color_target_rects[i][0], Crop.get_img_cropped_to_bounds(parent_img, color_target_rects[i][1], min_size = (sqrt(ppsi)*MIN_CROP_SIZE_INCHES, sqrt(ppsi)*MIN_CROP_SIZE_INCHES))))

    print("len before third remove step: ", len(color_target_crops))

    '''needs to remove bad crops through kmeans.
    Run kmeans on the image and find where the clusetres are. Two of these cluseters should be
    near valid target and letter colors'''

    '''crop removal with false crop catcher needs a more aggressive threshold to be set.
    Rather than only training off of random crops selected from images as false positives,
    instead use actual false positives that were found in the images it was run on.'''

    #remove_crops_with_false_crop_catcher(color_target_crops)
    remove_crops_with_width_length_ratio(color_target_crops)

    ''' TO KILL REMAINDER OF FALSE POSITIVES:
    Train a decision tree or random forest
    Vector would be an assemblage of responses to various shape algorithm responses
    i.e. number harris corners, circle response score, etc.
    Possibly train a model that uses the colors present in the image as well'''


    print("final len: ", len(color_target_crops))

    centers = []
    for i in range(0, len(color_target_crops)):
        centers.append(color_target_rects[i][1].get_center())

    target_crops = []
    for i in range(0, len(color_target_crops)):
        target_crops.append(TargetCrop(parent_img, color_target_crops[i][1], image_timestamp, geo_stamps, color_target_crops[i][0], ppsi))

    '''target_crop_index = 0
    KMEANS_RUN_TIMES = 4
    MIN_DIST_TO_TARGET_COLOR = 20
    MIN_DIST_TO_ELIMINATE_CLUSTER_COLOR = 20
    target_colors = TargetColorReader.target_colors
    while target_crop_index < len(target_crops):
        num_valid_colors = 0
        crop_colors = numpy.array(target_crops[target_crop_index].crop_img).reshape((-1, 3))
        crop_colors = numpy.float32(crop_colors)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, KMEANS_RUN_TIMES, 1.0)
        ret, labels, color_clusters = cv2.kmeans(crop_colors, 3, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        i = 0
        new_color_clusters = []
        while i < len(color_clusters):
            smallest_dist = numpy.linalg.norm(color_clusters[i] - color_clusters[0])
            for j in range(1, len(color_clusters)):
                if i != j:
                    dist_to_color = numpy.linalg.norm(color_clusters[i] - color_clusters[j])
                    if dist_to_color < smallest_dist:
                        dist_to_color = smallest_dist
            if not smallest_dist < MIN_DIST_TO_ELIMINATE_CLUSTER_COLOR:
                new_color_clusters.append(color_clusters[i])
            i+=1

        color_clusters = numpy.asarray(new_color_clusters)

        for i in range(0, len(color_clusters)):
            closest_color = sorted(target_colors, key = lambda target_color: numpy.linalg.norm(numpy.array(target_color) - color_clusters[i]))[0]
            dist_to_closest_color = numpy.linalg.norm(color_clusters[i] - numpy.array(closest_color))
            if dist_to_closest_color < MIN_DIST_TO_TARGET_COLOR:
                num_valid_colors += 1
        if num_valid_colors < 2:
            del target_crops[target_crop_index]
        else:
            target_crop_index += 1'''




    if get_centers:
        return target_crops, centers

    return target_crops


def remove_crops_with_width_length_ratio(color_target_crops):
    i = 0
    while i < len(color_target_crops):
        ratio = 0
        if color_target_crops[i][1].size[0] > color_target_crops[i][1].size[1]:
            ratio = float(color_target_crops[i][1].size[0])/float(color_target_crops[i][1].size[1])
        else:
            float(color_target_crops[i][1].size[1])/float(color_target_crops[i][1].size[0])
        if ratio > WIDTH_LENGTH_CUTOFF_RATIO:
            del color_target_crops[i]
        else:
            i += 1

def remove_crops_with_false_crop_catcher(color_target_crops):
    i = 0
    while i < len(color_target_crops):
        is_false_positive = FalseCropCatcher.get_if_is_false_positive(color_target_crops[i][1], color_target_crops[i][1].load())
        if is_false_positive:
            del color_target_crops[i]
        else:
            i+=1

def remove_duplicate_imgs_by_proximity(color_target_crops, ppsi):
    if len(color_target_crops) > 1:
        min_pixel_distance_away = float(MIN_CROP_DIST_AWAY)*sqrt(ppsi)
        i = 0
        while i < len(color_target_crops):
            sorted_color_targets_by_proximity = sorted(color_target_crops, key = lambda crop : numpy.linalg.norm(crop[0]-color_target_crops[i][0]))
            '''the second instance from the sorted list will be compared to since
            the first one will always be the crop to which we are comparing'''
            smallest_dist = numpy.linalg.norm(sorted_color_targets_by_proximity[1][0] - color_target_crops[i][0])
            if smallest_dist < min_pixel_distance_away:
                area_iter = color_target_crops[i][1].get_width() * color_target_crops[i][1].get_height()
                area_compare = sorted_color_targets_by_proximity[1][1].get_width() * sorted_color_targets_by_proximity[1][1].get_height()
                if area_iter < area_compare:
                    del color_target_crops[i]
                else:
                    remove_index = 0
                    removed = False
                    j = 0
                    while j < len(color_target_crops) and removed == False:
                        if numpy.linalg.norm(sorted_color_targets_by_proximity[1][0] - color_target_crops[j][0]) == 0:
                            del color_target_crops[j]
                            removed = True
                        j+=1
                    #i += 1
            else:
                i += 1


def remove_crops_by_area(color_target_crops, ppsi):
    i = 0
    num_removed_under_bounds = 0
    num_removed_over_bounds = 0
    while i < len(color_target_crops):
        pixel_area = color_target_crops[i][1].get_width() * color_target_crops[i][1].get_height()#color_target_crops[i][1].size[0] * color_target_crops[i][1].size[1]
        sqr_inch_area = float(pixel_area)/ppsi
        if not(sqr_inch_area > MIN_MAX_CROP_AREA_INCHES[0] and sqr_inch_area < MIN_MAX_CROP_AREA_INCHES[1]):
            del color_target_crops[i]

        if sqr_inch_area < MIN_MAX_CROP_AREA_INCHES[0]:
            num_removed_under_bounds += 1
        elif sqr_inch_area > MIN_MAX_CROP_AREA_INCHES[1]:
            num_removed_over_bounds += 1
        else:
            i += 1
    print("num removed under bounds: ", num_removed_under_bounds, ", num removed over bounds: ", num_removed_over_bounds)

def create_local_variance_image(image):
    '''find a way to use a sum table so that it doesn't have to sum things it has already summed
    https://stackoverflow.com/questions/18419871/improving-code-efficiency-standard-deviation-on-sliding-windows
    '''
    '''
    local_std_dev_image = numpy.zeros((image.shape[0], image.shape[1]))
    for x in range(LOCAL_VARIANCE_KERNEL_MARGIN, local_std_dev_image.shape[0] - LOCAL_VARIANCE_KERNEL_MARGIN):
        for y in range(LOCAL_VARIANCE_KERNEL_MARGIN, local_std_dev_image.shape[1] - LOCAL_VARIANCE_KERNEL_MARGIN):
            window_arr = image[x - LOCAL_VARIANCE_KERNEL_MARGIN : x + LOCAL_VARIANCE_KERNEL_MARGIN + 1, y - LOCAL_VARIANCE_KERNEL_MARGIN : y + LOCAL_VARIANCE_KERNEL_MARGIN + 1]
            mean, std_dev = cv2.meanStdDev(window_arr)
            local_std_dev_image[x,y] = numpy.linalg.norm(std_dev)
    return numpy.square(local_std_dev_image)'''
    c1 = uniform_filter(image, LOCAL_VARIANCE_KERNEL_MARGIN*2, mode='constant', origin=-LOCAL_VARIANCE_KERNEL_MARGIN)
    c2 = uniform_filter(image*image, LOCAL_VARIANCE_KERNEL_MARGIN*2, mode='constant', origin=-LOCAL_VARIANCE_KERNEL_MARGIN)
    out_image = ((c2 - c1*c1)**.5)[:-LOCAL_VARIANCE_KERNEL_MARGIN*2+1,:-LOCAL_VARIANCE_KERNEL_MARGIN*2+1]
    return numpy.square(out_image)





def create_thresholded_local_variance_img(local_variance_image):
    image = numpy.zeros((local_variance_image.shape[0], local_variance_image.shape[1]))
    for x in range(0, local_variance_image.shape[0]):
        for y in range(0, local_variance_image.shape[1]):
            if local_variance_image[x,y] > LOCAL_VARIANCE_THRESHOLD:
                image[x,y] = 255
    return Image.fromarray(image)
