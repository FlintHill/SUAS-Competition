
from ImgProcessingCLI.Runtime.TargetCrop import TargetCrop
import ImgProcessingCLI.Color.TargetColorReader as TargetColorReader
import ImgProcessingCLI.Color.ColorMath as ColorMath
import numpy
import ImgProcessingCLI.ImageOperation.Scale as Scale
from PIL import Image
import cv2
from math import sqrt, pi
import ImgProcessingCLI.ImageOperation.Crop as Crop
from ImgProcessingCLI.Geometry.Rectangle import Rectangle
import ImgProcessingCLI.TargetTrait.FalseCropCatcher as FalseCropCatcher
import timeit
import scipy
from scipy.ndimage.filters import uniform_filter
from scipy.ndimage.filters import convolve
import ImgProcessingCLI.Color.TargetColorReader as TargetColorReader

SALIENCY_MEDIAN_BLUR_RUN_TIMES = 3#5
SALIENCY_MEDIAN_BLUR_KERNEL_SIZE = 13
SALIENCY_MAP_SIDE_CONSTRAINT = 1620
SALIENCY_BLUR_SUBTRACTION_KERNEL_SIZE = 21
SALIENCY_BLUR_SECOND_PASS_KERNEL_SIZE = 3
SALIENCY_BLUR_SECOND_PASS_RUN_TIMES = 5



'''both of normalized saliency threshold bounds are tuned to a range of 0 - 255'''
NORMALIZED_SALIENCY_THRESHOLD_BOUNDS = (20, 200)#(20, 200)#(40, 170)

TARGET_IMAGE_INCHES_MARGIN = 6.0

class TargetCropperCrop:
    def __init__(self, parent_img, bounding_rect):
        self.img = parent_img.crop(bounding_rect)
        self.bounding_rect = bounding_rect
        self.midpoint = numpy.array([bounding_rect[0]+bounding_rect[2], bounding_rect[1] + bounding_rect[3]])/2.0

    '''returns one of the four corners of target_cropper_crop is within this crop's bounding rectangle. (so smaller rectangle inside bigger one)
    , the bigger one would not be considered within the bounds of the smaller one, but the smaller one would be considered in bounds of the bigger
    one'''
    def target_cropper_crop_inside_bounds(self, target_cropper_crop):
        bounding_p1 = numpy.array([target_cropper_crop.bounding_rect[0], target_cropper_crop.bounding_rect[1]])
        bounding_p2 = numpy.array([target_cropper_crop.bounding_rect[2], target_cropper_crop.bounding_rect[1]])
        bounding_p3 = numpy.array([target_cropper_crop.bounding_rect[2], target_cropper_crop.bounding_rect[3]])
        bounding_p4 = numpy.array([target_cropper_crop.bounding_rect[0], target_cropper_crop.bounding_rect[3]])
        target_cropper_crop_bounding_points = [bounding_p1, bounding_p2, bounding_p3, bounding_p4]
        for i in range(0, len(target_cropper_crop_bounding_points)):
            iter_point = target_cropper_crop_bounding_points[i]
            if iter_point[0] > self.bounding_rect[0] and iter_point[0] < self.bounding_rect[2] and iter_point[1] > self.bounding_rect[1] and iter_point[1] < self.bounding_rect[3]:
                return True
        return False

    def dist_to_target_cropper_crop(self, target_cropper_crop):
        return numpy.linalg.norm(target_cropper_crop.midpoint - self.midpoint)

    def img_pixel_area_within_bounds(self, lower_area, upper_area):
        img_area = self.img.size[0] * self.img.size[1]
        return img_area > lower_area and img_area < upper_area

    '''finds whether the ratio between the larger image dimension / the smaller image dimension is greater than the
    threshold ratio'''
    def img_dims_within_ratio(self, thresh_ratio):
        larger_dim = self.img.size[0]
        smaller_dim = self.img.size[1]
        if self.img.size[1] > self.img.size[0]:
            larger_dim = self.img.size[1]
            smaller_dim = self.img.size[0]
        ratio = float(larger_dim)/float(smaller_dim)
        return not (ratio > thresh_ratio)


    def show(self):
        self.img.show()


'''the following is the final Target Cropper I (Peter) made. As far as I can tell it has all of the framework for being an incredibly
resilient cropper. It works using an initial saliency map, but that alone is not enough for good detections as it is prone to false
positives.

As such, the algorithm operates almost like an ensemble algorithm, instead aggregating all instances of closed contours that are
contained within thresholded regions of saliency from the saliency map. Various false positive measures are taken (and generally
described as comments within the method or are relatively intuitive) as to how they work.

For sake of bettering future teams, I figured I might as well lay out the current pitfalls of the algorithm, and how they can be improved.
1: Saliency map is normalized and all thresholds are based off of that. This is flawed because, if an "especially interesting" (with
respect to saliency) image is inputted, good targets are likely to be weeded out as not "interesting" enough in favor of more salient
features in the abnormal image. All targets should have a general range of saliency no matter the image they appear on, and it is probably
best not to tune the algorithm using a normalized saliency map from 0 - 255.
2: Vulnerable to camera mis-colorations. Raw images do not appear in the same form as the generated test set we created, so it is
difficult to tune parameters. Make SURE the test data you use almost perfectly matches the input from competition to improve resiliency
and detection rate'''
def get_target_crops_from_img_final(parent_img, img_timestamp, geo_stamps, ppsi, get_centers = False):
    saliency_input_img = Scale.get_img_scaled_to_one_bound(parent_img, SALIENCY_MAP_SIDE_CONSTRAINT)

    saliency_input = numpy.array(saliency_input_img)
    #saliency_input = cv2.GaussianBlur(saliency_input, (7,7), 2.0)
    saliency_sub_blurred_image = cv2.GaussianBlur(saliency_input, (21, 21), 4.0)#cv2.blur(saliency_input, (SALIENCY_BLUR_SUBTRACTION_KERNEL_SIZE, SALIENCY_BLUR_SUBTRACTION_KERNEL_SIZE))
    saliency_map = saliency_input - saliency_sub_blurred_image
    saliency_map = numpy.linalg.norm(saliency_map, axis = 2)

    '''saliency map is normalized to 0 - 255 as this range is what the thresholds are tuned to'''
    thresh_saliency_map = numpy.uint8(255.0 * saliency_map/numpy.amax(saliency_map))

    '''threshold the saliency map so "disinteresting" points are eliminated -- effectively sets all relatively-certain-to-be-unimportant
    pixels to black'''
    thresh_saliency_map[thresh_saliency_map < NORMALIZED_SALIENCY_THRESHOLD_BOUNDS[0]] = 0
    thresh_saliency_map[thresh_saliency_map > NORMALIZED_SALIENCY_THRESHOLD_BOUNDS[1]] = 0

    for median_blur_run_count in range(0, SALIENCY_MEDIAN_BLUR_RUN_TIMES):
        thresh_saliency_map = cv2.medianBlur(thresh_saliency_map, SALIENCY_MEDIAN_BLUR_KERNEL_SIZE)

    '''converts the saliency map into a binary image'''
    thresh_saliency_map[thresh_saliency_map > 0] = 255

    '''thresh saliency map is mean blurred to expand the size of the blobs present in it. It is then thresholded again, effectively
    growing all blobs'''
    for second_pass_blur_count in range(0, SALIENCY_BLUR_SECOND_PASS_RUN_TIMES):
        thresh_saliency_map = cv2.blur(thresh_saliency_map, (SALIENCY_BLUR_SECOND_PASS_KERNEL_SIZE, SALIENCY_BLUR_SECOND_PASS_KERNEL_SIZE))
        thresh_saliency_map[thresh_saliency_map > 0] = 255

    '''cv2.imshow('thresh saliency map', thresh_saliency_map)
    cv2.waitKey(500)'''
    '''finding contours thresholds and presets:'''
    GAUSSIAN_KERNEL_SIZE = (7,7)
    GAUSSIAN_STD_DEV = 1.0
    CONTOUR_DOWNSCALE_CONSTRAINT = 1200
    CANNY_THRESHOLDS = (50, 100)#(100, 150)
    CANNY_APERTURE_SIZE = 3

    CONTOUR_BILAT_FILTER_THRESHOLDS = (15, 40, 40)
    CONTOUR_MEDIAN_BLUR_RUN_TIMES = 4
    CONTOUR_MEDIAN_BLUR_KERNEL_SIZE = 3

    '''is the image that is subtracted from canny, which essentially chops contours outside of the bounds off.
    Assumes the thresholded areas are bigger than the contours that they correlate to'''
    canny_subtraction_map = 255 - thresh_saliency_map

    canny_subtraction_map = numpy.array(Scale.get_img_scaled_to_one_bound(Image.fromarray(canny_subtraction_map), CONTOUR_DOWNSCALE_CONSTRAINT))

    contour_input_img = Scale.get_img_scaled_to_one_bound(parent_img, CONTOUR_DOWNSCALE_CONSTRAINT)
    contour_downscale_multiplier = float(contour_input_img.size[0])/float(parent_img.size[0])
    contour_upscale_multiplier = 1.0/contour_downscale_multiplier

    contour_input_image = numpy.array(contour_input_img)
    contour_input_image = cv2.bilateralFilter(contour_input_image, CONTOUR_BILAT_FILTER_THRESHOLDS[0], CONTOUR_BILAT_FILTER_THRESHOLDS[1], CONTOUR_BILAT_FILTER_THRESHOLDS[2])
    for i in range(0, CONTOUR_MEDIAN_BLUR_RUN_TIMES):
        contour_input_image = cv2.medianBlur(contour_input_image, CONTOUR_MEDIAN_BLUR_KERNEL_SIZE)

    '''try rgb canny as well as grayscale'''
    #contour_input_image = cv2.cvtColor(contour_input_image, cv2.COLOR_RGB2GRAY)

    blurred_contour_input_image = cv2.GaussianBlur(contour_input_image, GAUSSIAN_KERNEL_SIZE, GAUSSIAN_STD_DEV)
    contour_canny_image = cv2.Canny(blurred_contour_input_image, CANNY_THRESHOLDS[0], CANNY_THRESHOLDS[1], apertureSize = CANNY_APERTURE_SIZE)

    contour_input_image = contour_canny_image.copy()
    '''essentially subtracts the canny subtraction map. Actual subtraction was giving weird results with findContours (maybe the image was negative)
    somewhere...'''
    contour_input_image[canny_subtraction_map > 0] = 0
    #Image.fromarray(contour_input_image).show()
    #Image.fromarray(thresh_saliency_map).show()
    '''finds all contours in the canny image with the previously determined saliency
    map subtracted.
    Any contour at index i whose corresponding hierarchy[0][i][2] >= 0 is a closed-loop
    contour. The following determines all closed loop contours'''
    contour_image, contours, contours_hierarchy = cv2.findContours(contour_input_image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

    if len(contours) == 0:
        if get_centers:
            return [],[]
        return []

    closed_contours = []
    for i in range(0, contours_hierarchy.shape[1]):
        if contours_hierarchy[0][i][2] >= 0:
            closed_contours.append(contours[i])
    ROTATED_BOUNDING_DIM_RATIO_THRESHOLD = 2.5#2.0
    AREA_THRESHOLD_INCHES = (576.0, 28952.89344)#area of a 18in base triangle and area of 8 ft circle respectively.
    CONTOUR_AREA_THRESHOLDS = (AREA_THRESHOLD_INCHES[0] * ppsi / float(contour_upscale_multiplier**2), AREA_THRESHOLD_INCHES[1] * ppsi / float(contour_upscale_multiplier**2))
    '''removes all contours whose shape they contain are above or below the allowed area thresholds'''
    contour_index = 0
    while contour_index < len(closed_contours):
        blank_image = numpy.zeros(contour_canny_image.shape[0:2])
        filled_contour_image = cv2.drawContours(blank_image, closed_contours, contour_index, 1, thickness = cv2.FILLED)
        '''SOLUTION TO ISSUES with RUNWAY STRIPES:
        FIND THE MINIMUM AREA BOUNDING RECTANGLE OF THE FILLED CONTOUR. FIND OUT IF THIS MINIMUM AREA
        BOUNDING BOX IS VERY LONG AND THIN. THIS MEANS THAT IT IS LIKELY A RUNWAY STRIPE'''
        contour_area = numpy.sum(filled_contour_image)

        min_area_contour_bounding_rect = cv2.minAreaRect(closed_contours[contour_index])
        greater_rotated_bounding_dim = min_area_contour_bounding_rect[1][0]
        smaller_rotated_bounding_dim = min_area_contour_bounding_rect[1][1]
        if smaller_rotated_bounding_dim > greater_rotated_bounding_dim:
            greater_rotated_bounding_dim = min_area_contour_bounding_rect[1][1]
            smaller_rotated_bounding_dim = min_area_contour_bounding_rect[1][0]

        rotated_bounding_dim_ratio = float(greater_rotated_bounding_dim) / float(smaller_rotated_bounding_dim)

        if contour_area < CONTOUR_AREA_THRESHOLDS[0] or contour_area > CONTOUR_AREA_THRESHOLDS[1]:
            print("contour deleted by contour area thresholding")
            del closed_contours[contour_index]
        elif rotated_bounding_dim_ratio > ROTATED_BOUNDING_DIM_RATIO_THRESHOLD:
            print("contour deleted by rotated bounding dim ratio thresholding")
            del closed_contours[contour_index]
        else:
            contour_index += 1

    TARGET_IMAGE_PIXEL_MARGIN = TARGET_IMAGE_INCHES_MARGIN*sqrt(ppsi)
    bounding_contour_rects = []
    for i in range(0, len(closed_contours)):
        append_rect = ((numpy.array(cv2.boundingRect(closed_contours[i]))*contour_upscale_multiplier))
        '''converts the rectangle format from x1, y1, width, heith to
        x1, y1, x2, y1'''
        append_rect += numpy.array([0,0,append_rect[0], append_rect[1]])
        append_rect += numpy.array([-TARGET_IMAGE_PIXEL_MARGIN, -TARGET_IMAGE_PIXEL_MARGIN, TARGET_IMAGE_PIXEL_MARGIN, TARGET_IMAGE_PIXEL_MARGIN])
        append_rect = append_rect.astype(numpy.float)
        '''makes sure crop rectangle isn't out of bounds of the image'''
        if append_rect[0] < 0:
            append_rect[0] = 0
        if append_rect[1] < 0:
            append_rect[1] = 0
        if append_rect[2] > parent_img.size[0]:
            append_rect[2] = parent_img.size[0]
        if append_rect[3] > parent_img.size[1]:
            append_rect[3] = parent_img.size[1]
        bounding_contour_rects.append(tuple(append_rect.tolist()))

    cropper_crops = []
    for i in range(0, len(bounding_contour_rects)):
        cropper_crops.append(TargetCropperCrop(parent_img, bounding_contour_rects[i]))

    '''removes cropper crops if they do not satisfy various thresholding methods, including area,
    dimension ratio (i.e. a picture is too long and thin), etc.'''

    IMG_DIM_AREA_INCH = ((24.0**2) - (TARGET_IMAGE_INCHES_MARGIN **2), (96.0**2) - (TARGET_IMAGE_INCHES_MARGIN **2))#holds the minimum and maximum square area of targets in inches for use of removing them by the image dimension area
    IMG_DIM_AREA_THRESHOLDS = (IMG_DIM_AREA_INCH[0] * ppsi, IMG_DIM_AREA_INCH[1] * ppsi)
    IMG_DIM_RATIO = 3.0

    cropper_crop_index = 0
    while cropper_crop_index < len(cropper_crops):
        if not cropper_crops[cropper_crop_index].img_pixel_area_within_bounds(IMG_DIM_AREA_THRESHOLDS[0], IMG_DIM_AREA_THRESHOLDS[1]):
            #print("crop removed by image dimension area")
            del cropper_crops[cropper_crop_index]
        elif not cropper_crops[cropper_crop_index].img_dims_within_ratio(IMG_DIM_RATIO):
            #print("crop removed by image dimension ratio thresholding")
            del cropper_crops[cropper_crop_index]
        else:
            cropper_crop_index += 1


    '''try just vanilla connected components on the saliency thresholded map previously
    calculated???
    Also try: eliminate connected components in saliency map with too small or too large
    area'''

    '''crops must first be removed by size, as it is possible for a
    too-large crop to engulf the smaller, then the smaller, correct
    one is deleted by the below deletion'''

    base_crop_index = 0
    while base_crop_index < len(cropper_crops):
        compare_crop_index = 0
        while compare_crop_index < len(cropper_crops):
            if compare_crop_index != base_crop_index:
                compare_crop_in_base_crop = cropper_crops[base_crop_index].target_cropper_crop_inside_bounds(cropper_crops[compare_crop_index])
                '''if the compare crop is within the bounds of the base crop, delete the compare crop'''
                if compare_crop_in_base_crop:
                    del cropper_crops[compare_crop_index]
                    if compare_crop_index < base_crop_index:
                        base_crop_index -=1
                else:
                    compare_crop_index += 1
            else:
                compare_crop_index += 1

        base_crop_index += 1

    '''
    for i in range(0, len(cropper_crops)):
        cv2.imshow('hi', numpy.array(cropper_crops[i].img))
        cv2.waitKey(1000)'''

    target_crops_out = []
    target_centers_out = []
    for i in range(0, len(cropper_crops)):
        iter_target_midpoint = tuple(cropper_crops[i].midpoint.astype(numpy.int).tolist())
        append_target_crop = TargetCrop(parent_img, cropper_crops[i].img, img_timestamp, geo_stamps, iter_target_midpoint, ppsi)
        target_crops_out.append(append_target_crop)
        target_centers_out.append(iter_target_midpoint)
    '''still left to do:
    remove BOTH(???) of crops if they are within a threshold, small distance of each other(suggests some random terrain that often pops up
    on runway with a pattern could be present???).
    To weed out tree foliage false positives, create a 1d histogram using the mean color of each crop,
    then take the distance of each pixel to the mean. Threshold based on the variance of the set'''
    if get_centers:
        return target_crops_out, target_centers_out
    return target_crops_out
