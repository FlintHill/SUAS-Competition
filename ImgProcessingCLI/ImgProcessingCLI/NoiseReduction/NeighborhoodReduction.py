from scipy import stats
import numpy
from collections import Counter
from PIL import Image

def get_img_with_pixels_to_neighborhood_mode(img, image, kernel_size):
    #print("format is: " + str(Image.MIME[img.format]))
    img_out = Image.new(img.mode, img.size)
    image_out = img_out.load()
    kernel_margin = int((kernel_size - 1)/2)
    for x in range(0, img.size[0]):
        for y in range(0, img.size[1]):
            colors = []
            for i in range(x-kernel_margin, x+kernel_margin):
                for j in range(y-kernel_margin, y+kernel_margin):
                    if i >= 0 and i < img.size[0] and j >= 0 and j < img.size[1]:
                        colors.append(image[i,j])
            counter = Counter(colors)
            most_common_color = counter.most_common(1)
            #print("most common color: " + str(most_common_color))

            image_out[x,y] = most_common_color[0][0]
    return img_out
