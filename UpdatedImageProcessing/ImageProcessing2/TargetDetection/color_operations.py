import sys
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

    @staticmethod
    def nullify_color_and_crop_to_target(captured_image, color_difference_threshold):
        stopping_x = []
        stopping_y = []
        captured_image = captured_image.convert("RGBA")
        pixel_access_captured_image = captured_image.load()
        threshold_color = TargetAnalyzer.find_rim_average_color(captured_image)

        to_eliminate = False
        for x in range(captured_image.width):
            color_found = False

            for y in range(1, captured_image.height):
                color_difference = ColorOperations.find_percentage_difference(threshold_color, pixel_access_captured_image[x, y])

                if (color_difference > color_difference_threshold):
                    stopping_y.append(y)
                    color_found = True
                    break
                else:
                    pixel_access_captured_image[x, y] = (255, 255, 255, 0)

            y = captured_image.height - 1
            while (y >= 0):
                color_difference = ColorOperations.find_percentage_difference(threshold_color, pixel_access_captured_image[x, y])

                if ((color_difference > color_difference_threshold) and (pixel_access_captured_image[x, y][3] != 0)):
                    stopping_y.append(y)
                    color_found = True
                    break
                else:
                    pixel_access_captured_image[x, y] = (255, 255, 255, 0)

                y -= 1

            if ((color_found == False) and (x > captured_image.width * 4 / 10) and (x < captured_image.width * 6 / 10)):
                to_eliminate = True
                break

        for y in range(captured_image.height):
            color_found = False

            for x in range(1, captured_image.width):
                color_difference = ColorOperations.find_percentage_difference(threshold_color, pixel_access_captured_image[x, y])

                if ((color_difference > color_difference_threshold) and (pixel_access_captured_image[x, y][3] != 0)):

                    stopping_x.append(x)
                    color_found = True
                    break
                else:
                    pixel_access_captured_image[x, y] = (255, 255, 255, 0)

            x = captured_image.width - 1
            while (x >= 0):
                color_difference = ColorOperations.find_percentage_difference(threshold_color, pixel_access_captured_image[x, y])

                if ((color_difference > color_difference_threshold) and (pixel_access_captured_image[x, y][3] != 0)):

                    stopping_x.append(x)
                    color_found = True
                    break
                else:
                    pixel_access_captured_image[x, y] = (255, 255, 255, 0)
                x -= 1

            if ((color_found == False) and (y > captured_image.height * 4 / 10) and (y < captured_image.height * 6 / 10)):
                to_eliminate = True
                break

        if (to_eliminate == True):
            return 0

        else:

            x_min = min(stopping_x)
            y_min = min(stopping_y)
            x_max = max(stopping_x)
            y_max = max(stopping_y)

            recaptured_image = captured_image.crop((x_min - 5, y_min - 5, x_max + 5, y_max + 5))
            pixel_access_recaptured_image = recaptured_image.load()

            for x in range(recaptured_image.width):
                for y in range(recaptured_image.height):
                    number_of_blanks_around = 0
                    try:
                        if (pixel_access_recaptured_image[x - 1, y][3] == 0):
                            number_of_blanks_around += 1
                    except:
                        pass

                    try:
                        if (pixel_access_recaptured_image[x - 2, y][3] == 0):
                            number_of_blanks_around += 2
                    except:
                        pass

                    try:
                        if (pixel_access_recaptured_image[x + 1, y][3] == 0):
                            number_of_blanks_around += 1
                    except:
                        pass

                    try:
                        if (pixel_access_recaptured_image[x + 2, y][3] == 0):
                            number_of_blanks_around += 2
                    except:
                        pass

                    try:
                        if (pixel_access_recaptured_image[x, y - 1][3] == 0):
                            number_of_blanks_around += 1
                    except:
                        pass

                    try:
                        if (pixel_access_recaptured_image[x, y - 2][3] == 0):
                            number_of_blanks_around += 2
                    except:
                        pass

                    try:
                        if (pixel_access_recaptured_image[x, y + 1][3] == 0):
                            number_of_blanks_around += 1
                    except:
                        pass

                    try:
                        if (pixel_access_recaptured_image[x, y + 2][3] == 0):
                            number_of_blanks_around += 2
                    except:
                        pass

                    if (number_of_blanks_around > 6):
                        pixel_access_recaptured_image[x, y] = (255, 255, 255, 0)

            stopping_x = []
            stopping_y = []
            for x in range(recaptured_image.width):
                for y in range(1, recaptured_image.height):
                    if (pixel_access_recaptured_image[x, y][3] != 0):
                        stopping_y.append(y)
                        break
                    else:
                        pixel_access_recaptured_image[x, y] = (255, 255, 255, 0)

                y = recaptured_image.height - 1
                while (y >= 0):
                    if (pixel_access_recaptured_image[x, y][3] != 0):
                        stopping_y.append(y)
                        break
                    else:
                        pixel_access_recaptured_image[x, y] = (255, 255, 255, 0)
                    y -= 1

            for y in range(recaptured_image.height):
                for x in range(1, recaptured_image.width):
                    if (pixel_access_recaptured_image[x, y][3] != 0):
                        stopping_x.append(x)
                        break
                    else:
                        pixel_access_recaptured_image[x, y] = (255, 255, 255, 0)

                x = recaptured_image.width - 1
                while (x >= 0):
                    if (pixel_access_recaptured_image[x, y][3] != 0):
                        stopping_x.append(x)
                        break
                    else:
                        pixel_access_recaptured_image[x, y] = (255, 255, 255, 0)
                    x -= 1

            x_min = min(stopping_x)
            y_min = min(stopping_y)
            x_max = max(stopping_x)
            y_max = max(stopping_y)

            return recaptured_image.crop((x_min - 5, y_min - 5, x_max + 5, y_max + 5))
