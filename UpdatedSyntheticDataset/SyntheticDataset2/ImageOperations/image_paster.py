from PIL import Image
import math

class ImagePaster(object):

    @staticmethod
    def paste_images(image1, image2):
        """
        Paste image2 onto image1 with image2 centered at the center of image1.
        :param image1: the image of the shape.
        :param image2: the image of the letter.
        :type image1: an image file
        :type image2: an image file
        """
        image1.paste(image2, (((image1.width/2)-(image2.width/2)), ((image1.height/2)-(image2.height/2))), image2)
        return image1

    @staticmethod
    def paste_images_triangle_angle_north(image1, image2):
        """
        For pasting a letter onto an equilateral triangle with one of its angles facing north.
        :param image1: the image of the shape.
        :param image2: the image of the letter.
        :type image1: an image file
        :type image2: an image file
        """
        image1.paste(image2, (((image1.width/2)-(image2.width/2)), (image1.height-(image1.width/3)-(image2.height/2))), image2)
        return image1

    @staticmethod
    def paste_images_triangle_angle_south(image1, image2):
        """
        For pasting a letter onto an equilateral triangle with one of its angles facing south.
        :param image1: the image of the shape.
        :param image2: the image of the letter.
        :type image1: an image file
        :type image2: an image file
        """
        image1.paste(image2, (((image1.width/2)-(image2.width/2)), ((image1.width/3)-(image2.height/2))), image2)
        return image1

    @staticmethod
    def paste_images_pentagon_angle_north(image1, image2):
        """
        For pasting a letter onto a star or pentagon with one of its angles facing north.
        :param image1: the image of the shape.
        :param image2: the image of the letter.
        :type image1: an image file
        :type image2: an image file
        """
        image1.paste(image2, (((image1.width/2)-(image2.width/2)), (image1.height-int(image1.height/2.5)-(image2.height/2))), image2)
        return image1

    @staticmethod
    def paste_images_pentagon_angle_south(image1, image2):
        """
        For pasting a letter onto a star or pentagon with one of its angles facing south.
        :param image1: the image of the shape.
        :param image2: the image of the letter.
        :type image1: an image file
        :type image2: an image file
        """
        image1.paste(image2, (((image1.width/2)-(image2.width/2)), (int(image1.height/2.5)-(image2.height/2))), image2)
        return image1

    @staticmethod
    def paste_images_quarter_circle_northeast(image1, image2):
        """
        For pasting a letter onto a quarter-circle with its angle facing northeast.
        :param image1: the image of the shape.
        :param image2: the image of the letter.
        :type image1: an image file
        :type image2: an image file
        """
        image1.paste(image2, ((image1.width-(int(image1.width/(2*math.sqrt(2))))-image2.width/2), (int(image1.height/(2*math.sqrt(2)))-image2.height/2)), image2)
        return image1

    @staticmethod
    def paste_images_quarter_circle_southeast(image1, image2):
        """
        For pasting a letter onto a quarter-circle with its angle facing southeast.
        :param image1: the image of the shape.
        :param image2: the image of the letter.
        :type image1: an image file
        :type image2: an image file
        """
        image1.paste(image2, ((image1.width-(int(image1.width/(2*math.sqrt(2))))-image2.width/2), ((image1.height-(int(image1.height/(2*math.sqrt(2))))-image2.height/2))), image2)
        return image1

    @staticmethod
    def paste_images_quarter_circle_southwest(image1, image2):
        """
        For pasting a letter onto a quarter-circle with its angle facing southwest.
        :param image1: the image of the shape.
        :param image2: the image of the letter.
        :type image1: an image file
        :type image2: an image file
        """
        image1.paste(image2, ((int(image1.width/(2*math.sqrt(2)))-image2.width/2), ((image1.height-(int(image1.height/(2*math.sqrt(2))))-image2.height/2))), image2)
        return image1

    @staticmethod
    def paste_images_quarter_circle_northwest(image1, image2):
        """
        For pasting a letter onto a quarter-circle with its angle facing northwest.
        :param image1: the image of the shape.
        :param image2: the image of the letter.
        :type image1: an image file
        :type image2: an image file
        """
        image1.paste(image2, ((int(image1.width/(2*math.sqrt(2)))-image2.width/2), (int(image1.height/(2*math.sqrt(2)))-image2.height/2)), image2)
        return image1
