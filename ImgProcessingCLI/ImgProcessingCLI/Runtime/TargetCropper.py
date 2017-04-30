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
import timeit

DOWNSCALE_CONSTRAINT = 600
LOCAL_VARIANCE_THRESHOLD = 2000#second number is the rgb threshold, the first number is the CIE LAB threshold #150
BILAT_FILTER_THRESHOLDS = (15, 40, 40)
LOCAL_VARIANCE_KERNEL_SIZE = 3
LOCAL_VARIANCE_KERNEL_MARGIN = (LOCAL_VARIANCE_KERNEL_SIZE-1)//2
MAX_SQUARE_CROP_BOUNDS = 200*sqrt(2)
'''small margin of error added'''
'''something is wrong with min_max_crop_area_inches, can't figure out what.
Probably just bad ppsi numbers being fed in'''
MIN_MAX_CROP_AREA_INCHES = (1, 100000000)#(300, 14400)
CONNECTED_COMPONENT_SIZE_THRESHOLDS = (20, 200)#used to be (38, 200)
CROP_MARGIN_INCHES = 6
MIN_CROP_SIZE_INCHES = 36
'''sometimes there are cases where the same crop can be created
multiple times. In order to prevent this, crops with midpoints
that are within this variable away from each other (in inches)
are removed'''
MIN_CROP_DIST_AWAY = 120

def get_target_crops_from_img2(parent_img, geo_stamps, ppsi, get_centers = False):
    print("AT THE START of img2")
    downsized_parent_image = numpy.array(Scale.get_img_scaled_to_one_bound(parent_img, DOWNSCALE_CONSTRAINT).convert('RGB'))
    print("DOWNSIZED PARENT IMAGE")

    downscale_multiplier = float(DOWNSCALE_CONSTRAINT)/float(parent_img.size[0])
    upscale_multiplier = 1.0/downscale_multiplier

    print("BEFORE BILATERAL FILTER")
    print(type(downsized_parent_image))
    #cv2.imwrite("test.png", downsized_parent_image)
    cv2.imread(downsized_parent_image)
    #cv2.GaussianBlur(numpy.array(downsized_parent_image), (5,5), 3)
    print("TESTING")
    bilat_downsized_parent_image = cv2.GaussianBlur(numpy.array(downsized_parent_image), (5,5), 3)#cv2.bilateralFilter(downsized_parent_image, BILAT_FILTER_THRESHOLDS[0], BILAT_FILTER_THRESHOLDS[1], BILAT_FILTER_THRESHOLDS[2])
    print("BEFORE create_local_variance_image")
    local_variance_image = create_local_variance_image(bilat_downsized_parent_image)
    print("BILATERAL FILTER DONE")
    thresholded_local_variance_img = create_thresholded_local_variance_img(local_variance_image)
    thresholded_local_variance_img = Image.fromarray(cv2.medianBlur(numpy.array(thresholded_local_variance_img), 3))

    #thresholded_local_variance_img.show()
    connected_components_map = cv2.connectedComponents(numpy.uint8(numpy.array(thresholded_local_variance_img).T), connectivity = 4)
    connected_components_map = connected_components_map[1]
    print("THRESHOLDED IMG & CONNECTED COMPONENTS COMPLETED")

    connected_components = ImageMath.convert_connected_component_map_into_clusters(connected_components_map)
    crop_masks = []
    for i in range(0, len(connected_components)):
        if len(connected_components[i]) > CONNECTED_COMPONENT_SIZE_THRESHOLDS[0] and len(connected_components[i]) < CONNECTED_COMPONENT_SIZE_THRESHOLDS[1]:
            crop_masks.append(ImageMath.get_connected_component_mask(thresholded_local_variance_img.size, connected_components[i]))
    #new_img = parent_img.crop((100,100,200,200))
    color_target_rects = []
    pixel_crop_margin = int(float(CROP_MARGIN_INCHES) * sqrt(ppsi))+1
    for i in range(0, len(crop_masks)):
        mask_bounding_rect = Crop.get_bw_img_bounds(crop_masks[i], crop_masks[i].load())
        '''for some reason adding a crop margin to the right and bottom edge to the crop requires more than just
        2* the crop margin. The *3 is to mitigate this, and seems to work'''
        parent_img_bounding_rect = Rectangle(int(upscale_multiplier * mask_bounding_rect.get_x()) - pixel_crop_margin, int(upscale_multiplier * mask_bounding_rect.get_y()) - pixel_crop_margin, int(upscale_multiplier * mask_bounding_rect.get_width()) + (3 * pixel_crop_margin), int(upscale_multiplier * mask_bounding_rect.get_height()) + (3 * pixel_crop_margin))
        #append_img = Crop.get_img_cropped_to_bounds(parent_img, parent_img_bounding_rect)
        crop_midpoint = parent_img_bounding_rect.get_center()
        color_target_rects.append((crop_midpoint, parent_img_bounding_rect))

    removal_start_time = timeit.default_timer()

    remove_duplicate_imgs_by_proximity(color_target_rects, ppsi)
    remove_crops_by_area(color_target_rects, ppsi)

    color_target_crops = []
    for i in range(0, len(color_target_rects)):
        color_target_crops.append((color_target_rects[i][0], Crop.get_img_cropped_to_bounds(parent_img, color_target_rects[i][1], min_size = (sqrt(ppsi)*MIN_CROP_SIZE_INCHES, sqrt(ppsi)*MIN_CROP_SIZE_INCHES))))

    remove_crops_with_false_crop_catcher(color_target_crops)

    if get_centers:
        centers = []
        for i in range(0, len(color_target_crops)):
            centers.append(color_target_rects[i][1].get_center())
        return centers

    '''further improvement ideas:
    kmeans to three, then sum the distances from each colors and set a threshold that will
    eliminate images whose kmeans clusters are fairly close to each other (less likely to
    hold a target)'''
    target_crops = []
    for i in range(0, len(color_target_crops)):
        target_crops.append(TargetCrop(parent_img, color_target_crops[i][1], geo_stamps, color_target_crops[i][0], ppsi))
    return target_crops






def remove_duplicate_imgs_by_proximity(color_target_crops, ppsi):
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
    while i < len(color_target_crops):
        pixel_area = color_target_crops[i][1].get_width() * color_target_crops[i][1].get_height()#color_target_crops[i][1].size[0] * color_target_crops[i][1].size[1]
        sqr_inch_area = float(pixel_area)/ppsi
        if not(sqr_inch_area > MIN_MAX_CROP_AREA_INCHES[0] and sqr_inch_area < MIN_MAX_CROP_AREA_INCHES[1]):
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

def create_local_variance_image(bilat_downsized_parent_image):
    local_variance_image = numpy.zeros((bilat_downsized_parent_image.shape[0], bilat_downsized_parent_image.shape[1]))
    for x in range(LOCAL_VARIANCE_KERNEL_MARGIN, local_variance_image.shape[0] - LOCAL_VARIANCE_KERNEL_MARGIN):
        for y in range(LOCAL_VARIANCE_KERNEL_MARGIN, local_variance_image.shape[1] - LOCAL_VARIANCE_KERNEL_MARGIN):
            window_arr = bilat_downsized_parent_image[x - LOCAL_VARIANCE_KERNEL_MARGIN : x + LOCAL_VARIANCE_KERNEL_MARGIN + 1, y - LOCAL_VARIANCE_KERNEL_MARGIN : y + LOCAL_VARIANCE_KERNEL_MARGIN + 1]
            mean, std_dev = cv2.meanStdDev(window_arr)
            local_variance_image[x,y] = numpy.linalg.norm(std_dev)#**2
    return numpy.square(local_variance_image)

def create_thresholded_local_variance_img(local_variance_image):
    image = numpy.zeros((local_variance_image.shape[0], local_variance_image.shape[1]))
    for x in range(0, local_variance_image.shape[0]):
        for y in range(0, local_variance_image.shape[1]):
            if local_variance_image[x,y] > LOCAL_VARIANCE_THRESHOLD:
                image[x,y] = 255
    return Image.fromarray(image)





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


    var_img = numpy.zeros((image.shape[0], image.shape[1]))
    for x in range(kernel_margin, var_img.shape[0]-kernel_margin):
        for y in range(kernel_margin, var_img.shape[1]-kernel_margin):
            sub_arr = image[x-kernel_margin:x+kernel_margin+1, y-kernel_margin:y+kernel_margin+1]

            mean, std_dev = (cv2.meanStdDev(sub_arr))
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
    max_area = 48400*3
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
    '''maybe, instead of summing the distance, use the area of the triangle that the three points make and threshold that'''
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
