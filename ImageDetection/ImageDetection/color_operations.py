import math

class ColorOperations(object):

    @staticmethod
    def find_distance(color_1, color_2):
        return math.sqrt(((color_1[0] - color_2[0]) ** 2) + ((color_1[1] - color_2[1]) ** 2) + ((color_1[2] - color_2[2]) ** 2))

    @staticmethod
    def find_percentage_difference(color_1, color_2):
        color_distance = ColorOperations.find_distance(color_1, color_2)
        return (color_distance / math.sqrt(((255) ** 2) + ((255) ** 2) + ((255) ** 2))) * 100
