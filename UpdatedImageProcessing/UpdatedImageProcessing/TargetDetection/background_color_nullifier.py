from PIL import Image
from .color_operations import ColorOperations
from .target_analyzer import TargetAnalyzer

class BackgroundColorNullifier(object):

    @staticmethod
    def recrop_target(captured_image):
        """
        Scan through a captured_image, recapture the image so that 5-pixel
        margins from any non-transparent colors are left on all four directions.

        :param captured_image: a captured image of a potential target

        :type captured_image: a PIL image

        :return: a recaptured PIL image
        """
        pixel_access_captured_image = captured_image.load()
        stopping_x = []
        stopping_y = []
        for x in range(captured_image.width):
            for y in range(1, captured_image.height):
                if (pixel_access_captured_image[x, y][3] != 0):
                    stopping_y.append(y)
                    break

            y = captured_image.height - 1
            while (y >= 0):
                if (pixel_access_captured_image[x, y][3] != 0):
                    stopping_y.append(y)
                    break
                y -= 1

        for y in range(captured_image.height):
            for x in range(1, captured_image.width):
                if (pixel_access_captured_image[x, y][3] != 0):
                    stopping_x.append(x)
                    break

            x = captured_image.width - 1
            while (x >= 0):
                if (pixel_access_captured_image[x, y][3] != 0):
                    stopping_x.append(x)
                    break
                x -= 1

        x_min = min(stopping_x)
        y_min = min(stopping_y)
        x_max = max(stopping_x)
        y_max = max(stopping_y)

        recaptured_image = captured_image.crop((x_min - 5, y_min - 5, x_max + 5, y_max + 5))
        return recaptured_image

    @staticmethod
    def nullify_color_and_recrop_target(captured_image, color_difference_threshold):
        """
        Scan through a captured_image, both line by line and column by column,
        starting from all four directions. During this process, if the current
        pixel under scanning is within the color_difference_threshold, this
        current pixel is set to transparent. Otherwise, the location of the
        current pixel is marked, and the elimination process on this specific
        line or column is finished.

        :param captured_image: a captured image of a potential target
        :param color_difference_threshold: the threshold percentage difference
                                           between colors for determining
                                           the boundary of the target.
        :type captured_image: a PIL image
        :type color_difference_threshold: int

        :return: a recaptured and color-nullified PIL image
        """
        stopping_x = []
        stopping_y = []
        captured_image = captured_image.convert("RGBA")
        pixel_access_captured_image = captured_image.load()
        threshold_color = TargetAnalyzer.find_rim_average_color(captured_image)

        initial_image_area = captured_image.width * captured_image.height
        empty_space_area = 0

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
                    if (pixel_access_captured_image[x, y][3] != 0):
                        pixel_access_captured_image[x, y] = (255, 255, 255, 0)
                        empty_space_area += 1

            y = captured_image.height - 1
            while (y >= 0):
                color_difference = ColorOperations.find_percentage_difference(threshold_color, pixel_access_captured_image[x, y])

                if ((color_difference > color_difference_threshold) and (pixel_access_captured_image[x, y][3] != 0)):
                    stopping_y.append(y)
                    color_found = True
                    break
                else:
                    if (pixel_access_captured_image[x, y][3] != 0):
                        pixel_access_captured_image[x, y] = (255, 255, 255, 0)
                        empty_space_area += 1

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
                    if (pixel_access_captured_image[x, y][3] != 0):
                        pixel_access_captured_image[x, y] = (255, 255, 255, 0)
                        empty_space_area += 1

            x = captured_image.width - 1
            while (x >= 0):
                color_difference = ColorOperations.find_percentage_difference(threshold_color, pixel_access_captured_image[x, y])

                if ((color_difference > color_difference_threshold) and (pixel_access_captured_image[x, y][3] != 0)):

                    stopping_x.append(x)
                    color_found = True
                    break
                else:
                    if (pixel_access_captured_image[x, y][3] != 0):
                        pixel_access_captured_image[x, y] = (255, 255, 255, 0)
                        empty_space_area += 1

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

            index = 0
            while (index < 5):
                pixel_access_recaptured_image = recaptured_image.load()
                increased_empty_space_area = 0
                for x in range(recaptured_image.width):
                    for y in range(recaptured_image.height):
                        number_of_blanks_around_1 = 0
                        number_of_blanks_around_2 = 0

                        if (pixel_access_recaptured_image[x, y][3] != 0):

                            coordinates_to_scan_1 = [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]
                            coordinates_to_scan_2 = [[x - 2, y], [x + 2, y], [x, y - 2], [x, y + 2]]

                            for index_1 in range(len(coordinates_to_scan_1)):
                                try:
                                    if (pixel_access_recaptured_image[coordinates_to_scan_1[index_1][0], coordinates_to_scan_1[index_1][1]][3] == 0):
                                        number_of_blanks_around_1 += 1
                                except:
                                    pass

                            for index_2 in range(len(coordinates_to_scan_2)):
                                try:
                                    if (pixel_access_recaptured_image[coordinates_to_scan_2[index_2][0], coordinates_to_scan_2[index_2][1]][3] == 0):
                                        number_of_blanks_around_2 += 1
                                except:
                                    pass

                            if ((number_of_blanks_around_1 >= 3) or (number_of_blanks_around_2 >= 4)):
                                pixel_access_recaptured_image[x, y] = (255, 255, 255, 0)
                                increased_empty_space_area += 1

                recaptured_image = BackgroundColorNullifier.recrop_target(recaptured_image)
                if (increased_empty_space_area == 0):
                    break

                index += 1

            return recaptured_image
