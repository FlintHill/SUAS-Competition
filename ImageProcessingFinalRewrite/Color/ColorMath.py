from math import sqrt
from PIL import Image
def get_dist_between_colors(c1, c2):
    return sqrt((c2[0]-c1[0])**2 + (c2[1]-c1[1])**2 + (c2[2]-c1[2])**2)

def get_closest_color_from_list(list_in, color):
    sorted_colors = sorted(list_in, key=lambda check_color: get_dist_between_colors(color, check_color))
    return sorted_colors[0]

def get_img_rounded_to_colors(img, image, colors):
    img_copy = Image.new("RGB", img.size)
    image_copy = img_copy.load()
    for x in range(0, img.size[0]):
        for y in range(0, img.size[1]):
            image_copy[x,y] = get_closest_color_from_list(colors, image[x,y])
    return img_copy