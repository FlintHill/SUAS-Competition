import ImgProcessingCLI.KernelOperations.KernelMath as KernelMath
import numpy
from PIL import Image
import ImgProcessingCLI.KernelOperations.ScaleSpace as ScaleSpace
import ImgProcessingCLI.NoiseReduction.GaussianBlur as GaussianBlur
from math import exp, sqrt
from scipy.misc import imresize
from ImgProcessingCLI.Geometry.Rectangle import Rectangle
import ImgProcessingCLI.ImageOperation.Crop as Crop


BLOB_KERNEL = [[1.0,1.0,1.0], [1.0,-8.0,1.0], [1.0,1.0,1.0]]
def get_blob_crops_from_scale_space_imgs(img, scale_space, t_key, min_radius, max_radius, response_threshold = 100):
    blob_arrs = []
    t_range = get_t_range(min_radius, max_radius)
    start_index = -1

    for i in range(0, len(scale_space)):
        if t_key[i] > t_range[0] and t_key[i] < t_range[1]:
            if start_index == -1:
                start_index = i
            append_img = KernelMath.convolute_array(scale_space[i], BLOB_KERNEL)
            arr = numpy.array(append_img)
            arr = numpy.abs(arr) * t_key[i]
            blob_arrs.append(arr)

    scale_fit_blob_arrs(blob_arrs, scale_space)
    maxes = get_rel_maxes(blob_arrs, response_threshold, t_key[start_index:])
    #draw_maxes_to_img(img, blob_arrs, maxes).show()
    blob_rects = get_blob_rectangles(img.size, blob_arrs, maxes)

    copy_img = img.convert('RGB')
    copy_image = copy_img.load()
    for i in range(0, len(blob_rects)):
        blob_rects[i].draw(copy_img, copy_image, (255,0,0))
    copy_img.show()

    blob_rect_clusters = cluster_blob_rects(blob_rects)
    biggest_cluster = sorted(blob_rect_clusters, key = lambda cluster : len(cluster), reverse = True)

    bounded_clustered_blob_rects = get_cluster_bounding_boxes(blob_rect_clusters)


    img_copy = img.convert('RGB')
    image_copy = img_copy.load()
    for i in range(0, len(bounded_clustered_blob_rects)):
        bounded_clustered_blob_rects[i].draw(img_copy, image_copy, (0,0,255))
    img_copy.show()

    crops = []
    for i in range(0, len(bounded_clustered_blob_rects)):
        crops.append(Crop.get_img_cropped_to_bounds(img, bounded_clustered_blob_rects[i]))
    return crops


    #print("max val of: ", max, " at r: ", sqrt(t_key[max_index])*1.414*t_key[max_index])
    #print("max radius: ", (sqrt(t_key[len(t_key)-1]))*1.414*t_key[len(t_key)-1])

def get_t_range(min_radius, max_radius):
    return (((float(min_radius)**2)/2.0)**(1.0/3.0), ((float(max_radius)**2)/2.0)**(1.0/3.0))

def scale_fit_blob_arrs(blob_arrs, scale_space):
    for i in range(0, len(blob_arrs)):
        blob_arrs[i] = imresize(blob_arrs[i], blob_arrs[len(blob_arrs)-1].shape, interp = 'bicubic')
        #Image.fromarray(blob_arrs[i]).show()

'''response restriction is the whether the response is within the top n % of the max - the min of the whole thing.
In the future, replace with something that actually finds the top 50% of responses and takes the minimum
which will provide a better intensity threshold
'''
def get_rel_maxes(blob_arrs, response_threshold, t_key):

    maxes = []
    for arr_index in range(1, len(blob_arrs)-1):
        blob_arr = blob_arrs[arr_index]
        for x in range(1, blob_arr.shape[0]-1):
            for y in range(1, blob_arr.shape[1]-1):
                xy_val = blob_arr[x,y]
                if xy_val > response_threshold:
                    is_max = True
                    i = arr_index - 1
                    j = x - 1
                    k = y - 1
                    while i < arr_index + 2 and is_max:
                        while j < x + 2 and is_max:
                            while k < y + 2 and is_max:
                                if blob_arrs[i][j,k] >= xy_val and i != arr_index and j != x and k != y:
                                    is_max = False
                                k += 1
                            k = y - 1
                            j += 1
                        j = x - 1
                        i += 1
                    '''for i in range(arr_index - 1, arr_index + 2):
                        for j in range(x - 1, x + 2):
                            for k in range(y - 1, y + 2):
                                if blob_arrs[i][j,k] >= xy_val and i != arr_index and j != x and k != y:
                                    is_max = False'''

                    if is_max:
                        maxes.append((t_key[arr_index], x, y))
    return maxes

def get_blob_rectangles(original_img_size, blob_arrs, maxes):
    x_multiplier = float(original_img_size[0])/float(blob_arrs[len(blob_arrs)-1].shape[0])
    y_multiplier = float(original_img_size[1])/float(blob_arrs[len(blob_arrs)-1].shape[1])
    rects = []
    for i in range(0, len(maxes)):
        radius = sqrt(maxes[i][0])*1.414*maxes[i][0]
        rect = Rectangle(int(x_multiplier * maxes[i][1]-radius), int(y_multiplier * maxes[i][2]-radius), int(2*radius), int(2*radius))
        rects.append(rect)
    return rects


def cluster_blob_rects(rects):
    rects_copy = list(rects)
    clusters = []
    while len(rects_copy) > 0:
        if len(clusters) == 0:
            clusters.append([rects_copy[0]])
            del rects_copy[0]
        else:
            i = 0
            cluster_found = False
            while i < len(clusters) and not cluster_found:
                if get_if_rect_belongs_in_cluster(rects_copy[0], clusters[i]):
                    cluster_found = True
                    clusters[i].append(rects_copy[0])
                    del rects_copy[0]
                else:
                    i += 1
            if not cluster_found:
                clusters.append([rects_copy[0]])
                del rects_copy[0]
    return clusters

def get_cluster_bounding_boxes(rect_clusters):
    rects = []
    for i in range(0, len(rect_clusters)):
        rects.append(Rectangle.get_bounding_box_of_rectangles(rect_clusters[i]))
    return rects

def get_if_rect_belongs_in_cluster(rect, cluster):
    for i in range(0, len(cluster)):
        if rect.get_if_rect_overlaps(cluster[i]):
            return True
    return False
