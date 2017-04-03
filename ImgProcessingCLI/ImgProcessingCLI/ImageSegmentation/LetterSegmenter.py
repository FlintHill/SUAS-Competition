import numpy
import ImgProcessingCLI.KernelOperations.KernelMath as KernelMath
from PIL import Image



def get_segmented_letter_img(dim, mask_edge_image, canny_image):
    remove_shape_bounds_in_mask(dim, mask_edge_image)
    range_image = mask_edge_image#range_img.load()
    img = Image.new('L', dim)
    image = img.load()
    for y in range(0, dim[1]):
        mask_row_pixels = get_row_column_edges(dim, mask_edge_image, y, "right")
        if len(mask_row_pixels) > 1:
            row_range = (mask_row_pixels[0][0], mask_row_pixels[len(mask_row_pixels)-1][0])
            canny_image_row_edges = get_row_column_edges(dim, canny_image, y, "right", row_range)
            canny_image_row_edges = get_edges_with_clusters_cut_to_one(canny_image_row_edges)
            paint_between_edges(image, canny_image_row_edges, 255)

    for x in range(0, dim[0]):
        mask_column_pixels = get_row_column_edges(dim, mask_edge_image, x, "down")
        if len(mask_column_pixels) > 1:
            column_range = (mask_column_pixels[0][1], mask_column_pixels[len(mask_column_pixels)-1][1])
            canny_image_column_edges = get_row_column_edges(dim, canny_image, x, "down", column_range)
            canny_image_column_edges = get_edges_with_clusters_cut_to_one(canny_image_column_edges)
            paint_between_edges(image, canny_image_column_edges, 255)

    return img

def paint_between_edges(image, edges, color):
    numpy_edges = [numpy.array([edges[i][0], edges[i][1]]) for i in range(0, len(edges))]

    if len(edges)%2 == 0:
        for i in range(0, len(edges)-1):
            vec = numpy_edges[i+1]-numpy_edges[i]
            mag_vec = numpy.linalg.norm(vec)
            unit_vec = (1.0/mag_vec)*vec
            for t in range(0, int(mag_vec)):
                paint_pixel = numpy_edges[i] + unit_vec * t
                if i % 2 == 0:
                    image[paint_pixel[0], paint_pixel[1]] = color
                '''else:
                    if image[paint_pixel[0], paint_pixel[1]] == 0:
                        image[paint_pixel[0], paint_pixel[1]] = 128'''



def get_edges_with_clusters_cut_to_one(edges):
    out_edges = []
    for i in range(0, len(edges)):
        if edges[i][2] == "/":
            out_edges.append(edges[i])
    return out_edges
    '''out_edges = []
    out_edge_indexes = []
    for i in range(0, len(edges)):
        if edges[i][2] == True:
            if len(out_edges) == 0:
                out_edges.append(edges[i])
                out_edge_indexes.append(i)
            else:
                prev_cluster = get_connected_pixel_cluster(out_edge_indexes[len(out_edge_indexes)-1], edges)
                if not prev_cluster == get_connected_pixel_cluster(i, edges):
                    out_edges.append(edges[i])
                    out_edge_indexes.append(i)
        else:
            out_edges.append(edges[i])
            out_edge_indexes.append(i)

    return out_edges'''



def remove_shape_bounds_in_mask(dim, image):
    pixel_list = []
    for y in range(0, dim[1]):
        x_edges = get_row_column_edges(dim, image, y, "right")

        if len(x_edges) != 0:
            pixel_list.extend(get_connected_pixel_cluster(0, x_edges))
            pixel_list.extend(get_connected_pixel_cluster(len(x_edges)-1, x_edges))

    for x in range(0, dim[0]):
        y_edges = get_row_column_edges(dim, image, x, "down")
        if len(y_edges) != 0:
            pixel_list.extend(get_connected_pixel_cluster(0, y_edges))
            pixel_list.extend(get_connected_pixel_cluster(len(y_edges)-1, y_edges))

    paint_pixels(image, pixel_list, 0)


def remove_single_pixels_in_image(dim, image):
    kernel = [[1.0/255.0 for i in range(0, 3)] for j in range(0, 3)]

    for x in range(0, dim[0]):
        for y in range(0, dim[1]):
            if image[x,y] != 0:
                if KernelMath.get_kernel_sum_of_pixel((x,y), image, kernel) == 1:
                    image[x,y] = 0

def paint_pixels(image, pixels, color):
    for i in range(0, len(pixels)):
        image[int(pixels[i][0]), int(pixels[i][1])] = color

'''takes pixels that have been labeled and are in a tuple'''
def get_connected_pixel_cluster(base_pixel_index, edges):
    range = get_range_of_cluster_containing_pixel(base_pixel_index, edges)
    return edges[range[0]:range[1]+1]

def get_range_of_cluster_containing_pixel(pixel_index, edges):


    i = pixel_index
    end_found = False
    start_index = pixel_index
    end_index = pixel_index
    start_found = False
    if edges[pixel_index][2] == "/":
        start_found = True
        start_index = pixel_index
    elif edges[pixel_index][2] == "|":
        end_found = True
        end_index = pixel_index
    while i >= 0 and not start_found:
        if edges[i][2] == "/":
            start_found = True
            start_index = i
        if edges[i][2] == "|" and i != pixel_index:
            start_found = True

        i-=1
    i = pixel_index
    while i < len(edges) and not end_found:
        if edges[i][2] == "|":
            end_found = True
            end_index = i
        if edges[i][2] == "/" and i != pixel_index:
            end_found = True
        i+=1
    return (start_index, end_index)


'''def get_connected_pixel_cluster(base_pixel_index, edges):
    up_pixels = []
    end_of_cluster_found = False
    i = base_pixel_index
    if edges[base_pixel_index][2] == True:
        while i < len(edges)-1 and end_of_cluster_found == False:
            if(i != base_pixel_index):
                if edges[i][2] == True and get_if_pixels_neighbor(edges[i], edges[i+1]):
                    up_pixels.append(edges[i])
                else:
                    end_of_cluster_found = True
            i+=1

        down_pixels = []
        end_of_cluster_found = False
        i = base_pixel_index
        while i > 0 and end_of_cluster_found == False:
            if(i != base_pixel_index):
                if edges[i][2] == True and get_if_pixels_neighbor(edges[i], edges[i-1]):
                    down_pixels.append(edges[i])
                else:
                    end_of_cluster_found = True
            i-=1
        down_pixels = list(reversed(down_pixels))

        cluster = list(down_pixels)
        cluster.append(edges[base_pixel_index])
        cluster.extend(up_pixels)
        return cluster
    return [edges[base_pixel_index]]
  '''
def get_row_column_edges(dim, image, start_row_column, direction, range = None):
    edges = []

    current_pixel = numpy.array([0,0])
    if direction == "right":
        if range == None:
            current_pixel = numpy.array([0, start_row_column])
        else:
            current_pixel = numpy.array([range[0], start_row_column])
    else:
        if range == None:
            current_pixel = numpy.array([start_row_column, 0])
        else:
            current_pixel = numpy.array([start_row_column, range[0]])

    stop_iter = False
    while pixel_in_dim(dim, current_pixel) and stop_iter == False:
        if image[int(current_pixel[0]), int(current_pixel[1])] != 0:
            edges.append(numpy.copy(current_pixel))
        if direction == "right":
            current_pixel[0] += 1
            stop_iter = range != None and current_pixel[0] >= range[1]
        else:
            current_pixel[1] += 1
            stop_iter = range != None and current_pixel[1] >= range[1]
    return get_labeled_connected_pixels(edges)


def get_labeled_connected_pixels(edges):
    new_edges = [[edges[i][0], edges[i][1], "-"] for i in range(0, len(edges))]

    for i in range(0, len(edges)-1):
        if not get_if_pixels_neighbor(edges[i], edges[i+1]):
            if new_edges[i][2] != "/":
                new_edges[i][2] = "|"
            new_edges[i+1][2] = "/"

    if len(edges) != 0:
        new_edges[0][2] = "/"
    if len(edges) > 1:
        if get_if_pixels_neighbor(edges[len(edges)-2], edges[len(edges)-1]):
            new_edges[len(edges)-1][2] = "|"

    return new_edges

    '''for i in range(0, len(edges)):
        next_to_others = get_if_pixel_is_next_to_others_in_list(new_edges[i], edges)
        if next_to_others:
            new_edges[i] = [new_edges[i][0], new_edges[i][1], "-"]
        else:
            new_edges[i] = [new_edges[i][0], new_edges[i][1], "/"]

    discontinuity_indexes = []
    for i in range(0, len(edges)-1):
        if new_edges[i][2] == "-" and new_edges[i+1][2] == "-":
            if not get_if_pixels_neighbor(new_edges[i], new_edges[i+1]):
                discontinuity_indexes.append(i+1)

    for i in range(0, len(discontinuity_indexes)):
        new_edges[discontinuity_indexes[i]][2] = "|"

    start_indexes = []
    start_found = False
    for i in range(0, len(new_edges)-1):
        if not start_found and new_edges[i][2] == "-" and new_edges[i+1][2] == "-":
            start_found = True
            start_indexes.append(i)
        elif start_found:
            if new_edges[i][2] == "|":
                start_found = False

    for i in range(0, len(start_indexes)):
        new_edges[start_indexes[i]][2] = "/"

    print("edges are: " + str(edges))
    print("new edges are: " + str(new_edges))
    return new_edges
    '''


def get_if_pixel_is_next_to_others_in_list(pixel, edges):
    for i in range(0, len(edges)):
        if not (edges[i] == pixel).all():
            if get_if_pixels_neighbor(pixel, edges[i]):
                return True
    return False

def get_if_pixels_neighbor(pixel1, pixel2):
    if pixel1[0] == pixel2[0]:
        return (pixel1[1] == pixel2[1]+1 or pixel1[1] == pixel2[1]-1)
    elif pixel1[1] == pixel2[1]:
        return (pixel1[0] == pixel2[0]+1 or pixel1[0] == pixel2[0]-1)
    return False


def pixel_in_dim(dim, pixel):
    return (pixel[0] >= 0 and pixel[0] < dim[0] and pixel[1] >= 0 and pixel[1] < dim[1])
