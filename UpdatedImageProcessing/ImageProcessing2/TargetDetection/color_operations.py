import sys
import cv2
import numpy
import PIL.ImageOps
from PIL import Image
from sklearn.cluster import MiniBatchKMeans

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

    @staticmethod
    def nullify_color_and_crop_to_target(captured_image, quantized_image, color_difference_threshold):
        x_min = sys.maxint
        y_min = sys.maxint
        x_max = 0
        y_max = 0

        captured_image = captured_image.convert("RGBA")
        pixel_access_captured_image = captured_image.load()
        pixel_access_quantized_image = quantized_image.load()

        to_eliminate = False
        for x in range(quantized_image.width):
            threshold_color = pixel_access_quantized_image[x, 0]

            color_found = False

            for y in range(1, quantized_image.height):
                color_difference = ColorOperations.find_percentage_difference(threshold_color, pixel_access_quantized_image[x, y])

                if (color_difference > color_difference_threshold):
                    y_min = y
                    color_found = True
                    break
                else:
                    pixel_access_captured_image[x, y] = (255, 255, 255, 0)

            y = quantized_image.height - 1

            while (y >= 0):
                color_difference = ColorOperations.find_percentage_difference(threshold_color, pixel_access_quantized_image[x, y])

                if (color_difference > color_difference_threshold):
                    y_max = y
                    color_found = True
                    break
                else:
                    pixel_access_captured_image[x, y] = (255, 255, 255, 0)

                y -= 1

            if ((color_found == False) and (x > quantized_image.width * 4 / 10) and (x < quantized_image.width * 6 / 10)):
                to_eliminate = True
                break


        for y in range(quantized_image.height):
            threshold_color = pixel_access_quantized_image[0, y]

            color_found = False

            for x in range(1, quantized_image.width):
                color_difference = ColorOperations.find_percentage_difference(threshold_color, pixel_access_quantized_image[x, y])

                if (color_difference > color_difference_threshold):
                    x_min = x
                    color_found = True
                    break
                else:
                    pixel_access_captured_image[x, y] = (255, 255, 255, 0)

            x = quantized_image.width - 1

            while (x >= 0):
                color_difference = ColorOperations.find_percentage_difference(threshold_color, pixel_access_quantized_image[x, y])

                if (color_difference > color_difference_threshold):
                    x_max = x
                    color_found = True
                    break
                else:
                    pixel_access_captured_image[x, y] = (255, 255, 255, 0)

                x -= 1

            if ((color_found == False) and (y > quantized_image.height * 4 / 10) and (y < quantized_image.height * 6 / 10)):
                to_eliminate = True
                break

        if ((x_min == sys.maxint) or (y_min == sys.maxint) or (x_max == 0) or (y_max == 0)):
            to_eliminate = True

        if (to_eliminate == True):
            return 0

        else:
            x_min = x_min - 5
            y_min = y_min - 5
            x_max = x_max + 5
            y_max = y_max + 5

            captured_image.crop((x_min, y_min, x_max, y_max))
            return captured_image
