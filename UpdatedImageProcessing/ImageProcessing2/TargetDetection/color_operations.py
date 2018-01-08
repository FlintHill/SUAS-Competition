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
    def apply_color_quantization(rgb_image, kmeans_clusters_number):
        lab_image = cv2.cvtColor(numpy.array(rgb_image), cv2.COLOR_RGB2LAB)
        lab_image = lab_image.reshape((lab_image.shape[0] * lab_image.shape[1], 3))

        clt = MiniBatchKMeans(n_clusters = kmeans_clusters_number)
        labels = clt.fit_predict(lab_image)

        lab_image = clt.cluster_centers_.astype("uint8")[labels]
        lab_image = lab_image.reshape((rgb_image.height, rgb_image.width, 3))
        bgr_image = cv2.cvtColor(lab_image, cv2.COLOR_LAB2BGR)
        rgb_image = Image.fromarray(bgr_image, 'RGB')
        return rgb_image

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

        left_x = min(list_of_x)
        right_x = max(list_of_x)
        up_y = min(list_of_y)
        low_y = max(list_of_y)

        return (left_x - margin_length, up_y - margin_length, right_x + margin_length, low_y + margin_length)
