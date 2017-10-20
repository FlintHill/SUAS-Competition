from PIL import Image
import math
from SyntheticDataset2.ElementsCreator import *
from SyntheticDataset2.ImageOperations import *

class ImagePaster(object):

    @staticmethod
    def paste_images(image1, image2):
        """
        Paste image2 onto image1 with image2 centered at the center of image1.
        """
        image1.paste(image2, (((image1.width/2)-(image2.width/2)), ((image1.height/2)-(image2.height/2))), image2)
        return image1

    @staticmethod
    def paste_images_triangle_angle_north(image1, image2):
        """
        For pasting a letter onto an equilateral triangle with one of its angles pointing up.
        image2 is the image of the letter.
        image1 is the image of the shape.
        """
        image1.paste(image2, (((image1.width/2)-(image2.width/2)), (image1.height-(image1.width/3)-(image2.height/2))), image2)
        return image1

    @staticmethod
    def paste_images_triangle_angle_south(image1, image2):
        """
        For pasting a letter onto an equilateral triangle with one of its sides pointing up.
        image2 is the image of the letter.
        image1 is the image of the shape.
        """
        image1.paste(image2, (((image1.width/2)-(image2.width/2)), ((image1.width/3)-(image2.height/2))), image2)
        return image1

    @staticmethod
    def paste_images_pentagon_angle_north(image1, image2):
        """
        For pasting a letter onto a star with one of its convexes pointing up,
        or an equilateral pentagon with one of its angles pointing up.
        image2 is the image of the letter.
        image1 is the image of the shape.
        """
        image1.paste(image2, (((image1.width/2)-(image2.width/2)), (image1.height-int(image1.height/2.5)-(image2.height/2))), image2)
        return image1

    @staticmethod
    def paste_images_pentagon_angle_south(image1, image2):
        """
        For pasting a letter onto a star with one of its concaves pointing up,
        or an equilateral pentagon with one of its sides pointing up.
        image2 is the image of the letter.
        image1 is the image of the shape.
        """
        image1.paste(image2, (((image1.width/2)-(image2.width/2)), (int(image1.height/2.5)-(image2.height/2))), image2)
        return image1

    @staticmethod
    def paste_images_quarter_circle_northeast(image1, image2):
        """
        For pasting a letter onto a quarter-circle with its angle pointing up-right.
        image2 is the image of the letter.
        image1 is the image of the shape.
        """
        image1.paste(image2, ((image1.width-(int(image1.width/(2*math.sqrt(2))))-image2.width/2), (int(image1.height/(2*math.sqrt(2)))-image2.height/2)), image2)
        return image1

    @staticmethod
    def paste_images_quarter_circle_southeast(image1, image2):
        """
        For pasting a letter onto a quarter-circle with its angle pointing down-right.
        image2 is the image of the letter.
        image1 is the image of the shape.
        """
        image1.paste(image2, ((image1.width-(int(image1.width/(2*math.sqrt(2))))-image2.width/2), ((image1.height-(int(image1.height/(2*math.sqrt(2))))-image2.height/2))), image2)
        return image1

    @staticmethod
    def paste_images_quarter_circle_southwest(image1, image2):
        """
        For pasting a letter onto a quarter-circle with its angle pointing down-left.
        image2 is the image of the letter.
        image1 is the image of the shape.
        """
        image1.paste(image2, ((int(image1.width/(2*math.sqrt(2)))-image2.width/2), ((image1.height-(int(image1.height/(2*math.sqrt(2))))-image2.height/2))), image2)
        return image1

    @staticmethod
    def paste_images_quarter_circle_northwest(image1, image2):
        """
        For pasting a letter onto a quarter-circle with its angle pointing up-left.
        image2 is the image of the letter.
        image1 is the image of the shape.
        """
        image1.paste(image2, ((int(image1.width/(2*math.sqrt(2)))-image2.width/2), (int(image1.height/(2*math.sqrt(2)))-image2.height/2)), image2)
        return image1
