from PIL import Image
from math import cos, sin, pi

CANNY_RADIUS = 1.5
CANNY_VAL_45_DEG = CANNY_RADIUS * sin((pi/8.0))
THRESHOLD_COLOR = 128

'''takes a SobelEdge object, and thresholds in the form of: lower, upper'''
def get_canny_img(sobel_edge, thresholds):
    out_img = Image.new('L', sobel_edge.get_gradient_mag_img().size)
    out_image = out_img.load()
    for x in range(1, out_img.size[0] - 1):
        for y in range(1, out_img.size[1] - 1):
            if pixel_is_max_across_edge(sobel_edge, (x,y), sobel_edge.get_gradient_mags()[x][y], sobel_edge.get_gradient_angles()[x][y]) and sobel_edge.get_gradient_mags()[x][y] > thresholds[0]:
                out_image[x,y] = 255
    return basic_threshold_img(out_img, out_image, sobel_edge.get_gradient_mags(), thresholds[1])

def pixel_is_max_across_edge(sobel_edge, pixel, pixel_mag, angle):
    perp_angle = angle + (pi/4.0)
    neighbor_pixels = get_neighboring_edge_pixel_mags(sobel_edge, pixel, perp_angle)
    return (pixel_mag >= neighbor_pixels[0] and pixel_mag >= neighbor_pixels[1])

def get_neighboring_edge_pixel_mags(sobel_edge, pixel, perp_angle):
    xComp = CANNY_RADIUS * cos(perp_angle)
    yComp = CANNY_RADIUS * sin(perp_angle)
    dx = 0
    dy = 0
    if yComp > -CANNY_VAL_45_DEG and yComp < CANNY_VAL_45_DEG:
        dy = 0
    elif yComp >= CANNY_VAL_45_DEG:
        dy = 1
    elif yComp <= -CANNY_VAL_45_DEG:
        dy = -1

    if xComp > -CANNY_VAL_45_DEG and xComp < CANNY_VAL_45_DEG:
        dx = 0
    elif xComp >= CANNY_VAL_45_DEG:
        dx = 1
    elif xComp <= -CANNY_VAL_45_DEG:
        dx = -1
    firstPixel = (pixel[0] + dx, pixel[1] - dy)
    secondPixel = (pixel[0] - dx, pixel[1] + dy)
    return (sobel_edge.get_gradient_mags()[firstPixel[0]][firstPixel[1]], sobel_edge.get_gradient_mags()[secondPixel[0]][secondPixel[1]])

def basic_threshold_img(img, image, mag_gradients, lower_threshold):
    img_copy = img.copy()
    image_copy = img_copy.load()
    for x in range(1, img_copy.size[0] - 1):
        for y in range(1, img_copy.size[1] - 1):
            if image_copy[x,y] != 255 and mag_gradients[x][y] >= lower_threshold and pixel_surrounded_by_edges(image, (x,y), 2, 2):
                image_copy[x,y] = THRESHOLD_COLOR
    return  img_copy

def pixel_surrounded_by_edges(image, pixel, kernel_size, min_edges):
    edge_count = 0
    last_index = (-1,-1)
    for i in range(pixel[0] - int(kernel_size/2), pixel[0] + 1 + int(kernel_size/2)):
        for j in range(pixel[1] - int(kernel_size/2), pixel[1] + 1 + int(kernel_size/2)):
            if image[i,j] != 0:
                if (abs(j - last_index[1]) + abs(i - last_index[0])) > 2:
                    edge_count += 1
                    last_index = (i,j)
    return (edge_count >= min_edges)
