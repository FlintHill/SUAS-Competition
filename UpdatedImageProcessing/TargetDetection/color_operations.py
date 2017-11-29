import cv2
import math
import numpy
import PIL.ImageOps
from PIL import Image
from sklearn.cluster import MiniBatchKMeans

class ColorOperations(object):

    @staticmethod
    def find_distance(color_1, color_2):
        return math.sqrt(((color_1[0] - color_2[0]) ** 2) + ((color_1[1] - color_2[1]) ** 2) + ((color_1[2] - color_2[2]) ** 2))

    @staticmethod
    def find_percentage_difference(color_1, color_2):
        color_distance = ColorOperations.find_distance(color_1, color_2)
        return (color_distance / math.sqrt(((255) ** 2) + ((255) ** 2) + ((255) ** 2))) * 100

    @staticmethod
    def quantize_color(rgb_image, kmeans_clusters_number):
        (h, w) = (rgb_image.height, rgb_image.width)
        lab_image = cv2.cvtColor(numpy.array(rgb_image), cv2.COLOR_RGB2LAB)
        lab_image = lab_image.reshape((lab_image.shape[0] * lab_image.shape[1], 3))

        clt = MiniBatchKMeans(n_clusters = kmeans_clusters_number)
        labels = clt.fit_predict(lab_image)

        lab_image = clt.cluster_centers_.astype("uint8")[labels]
        lab_image = lab_image.reshape((h, w, 3))
        bgr_image = cv2.cvtColor(lab_image, cv2.COLOR_LAB2BGR)
        rgb_image = Image.fromarray(bgr_image, 'RGB')
        return rgb_image

    @staticmethod
    def find_boundary_of_color(image, color):
        dimension = image.size
        list_of_x = []
        list_of_y = []

        for x in range(dimension[0]):
            for y in range(dimension[1]):
                if image.load()[x, y] == color:
                    list_of_x.append(x)
                    list_of_y.append(y)

        left_x = min(list_of_x)
        right_x = max(list_of_x)
        up_y = min(list_of_y)
        low_y = max(list_of_y)
        return (left_x - 5, up_y - 5, right_x + 5, low_y + 5)

    @staticmethod
    def nullify_color_and_crop_to_target(captured_image, quantized_image, color_difference_threshold):
        x_min = 1000000
        y_min = 1000000
        x_max = 0
        y_max = 0

        captured_image = captured_image.convert("RGBA")

        for x in range(quantized_image.width):
            threshold_color = quantized_image.load()[x, 0]

            for y in range(1, quantized_image.height):
                color_difference = ColorOperations.find_percentage_difference(threshold_color, quantized_image.load()[x, y])

                if (color_difference > color_difference_threshold):
                    y_min = y
                    break

                else:
                    captured_image.load()[x, y] = (255, 255, 255, 0)

            y = quantized_image.height - 1
            while (y >= 0):
                color_difference = ColorOperations.find_percentage_difference(threshold_color, quantized_image.load()[x, y])

                if (color_difference > color_difference_threshold):
                    y_max = y
                    break

                else:
                    captured_image.load()[x, y] = (255, 255, 255, 0)

                y -= 1

        for y in range(quantized_image.height):
            threshold_color = quantized_image.load()[0, y]

            for x in range(1, quantized_image.width):
                color_difference = ColorOperations.find_percentage_difference(threshold_color, quantized_image.load()[x, y])

                if (color_difference > color_difference_threshold):
                    x_min = x
                    break

                else:
                    captured_image.load()[x, y] = (255, 255, 255, 0)

            x = quantized_image.width - 1
            while (x >= 0):
                color_difference = ColorOperations.find_percentage_difference(threshold_color, quantized_image.load()[x, y])

                if (color_difference > color_difference_threshold):
                    x_max = x
                    break

                else:
                    captured_image.load()[x, y] = (255, 255, 255, 0)

                x -= 1

        x_min = x_min - 5
        y_min = y_min - 5
        x_max = x_max + 5
        y_max = y_max + 5

        captured_image.crop((x_min, y_min, x_max, y_max))

        return captured_image
