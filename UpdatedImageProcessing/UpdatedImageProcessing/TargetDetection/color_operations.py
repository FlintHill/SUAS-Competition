import cv2
import numpy
import PIL.ImageOps
from PIL import Image
from sklearn.cluster import MiniBatchKMeans
from .target_analyzer import TargetAnalyzer

class ColorOperations(object):

    @staticmethod
    def find_distance(color_1, color_2):
        return numpy.sqrt([numpy.sum([(color_1[0] - color_2[0]) ** 2, (color_1[1] - color_2[1]) ** 2, (color_1[2] - color_2[2]) ** 2])])

    @staticmethod
    def find_percentage_difference(color_1, color_2):
        color_distance = ColorOperations.find_distance(color_1, color_2)
        return (color_distance / numpy.sqrt([3 * (255 ** 2)])) * 100

    @staticmethod
    def apply_mean_blur(rgb_image, kernel_size):
        rgb_image = numpy.array(rgb_image)
        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        bgr_image = cv2.blur(bgr_image, (kernel_size, kernel_size))
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        rgb_image = Image.fromarray(rgb_image)
        return rgb_image

    @staticmethod
    def apply_median_blur(rgb_image, kernel_size):
        rgb_image = numpy.array(rgb_image)
        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        bgr_image = cv2.medianBlur(bgr_image, kernel_size)
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        rgb_image = Image.fromarray(rgb_image)
        return rgb_image

    @staticmethod
    def find_boundary_of_color(image, color, margin_length):
        list_of_x = []
        list_of_y = []
        pixel_access_image = image.load()

        for x in range(image.size[0]):
            for y in range(image.size[1]):
                if pixel_access_image[x, y] == color:
                    list_of_x.append(x)
                    list_of_y.append(y)

        if ((len(list_of_x) == 0) or (len(list_of_y) == 0)):
            return -1

        left_x = min(list_of_x)
        right_x = max(list_of_x)
        up_y = min(list_of_y)
        low_y = max(list_of_y)

        if ((left_x - margin_length) < 0):
            final_left_x = 0
        else:
            final_left_x = left_x - margin_length

        if ((up_y - margin_length) < 0):
            final_up_y = 0
        else:
            final_up_y = up_y - margin_length

        if ((right_x + margin_length) >= image.width):
            final_right_x = image.width - 1
        else:
            final_right_x = right_x + margin_length

        if ((low_y + margin_length) >= image.height):
            final_low_y = image.height - 1
        else:
            final_low_y = low_y + margin_length

        return (final_left_x, final_up_y, final_right_x, final_low_y)
