from PIL import Image
import math

class ImageResizer(object):

    @staticmethod
    def resize_image_conserved(image, level_of_pixelization):
        """
        Downscale an image and then upscale the image by the same amount, creating a pixelized effect.
        When inputting a level of pixelization, this specific method outputs the same amount of pixelization
        regardless of the size of the image. In other words, the amount of resizing depends on the size of
        the image, if this is not intended, use the second method in this class.

        :param image: the image to be resized
        :param level_of_pixelization: the level of pixelization intended (below 20 recommended)
        :type image: an image file
        :type level_of_pixelization: float
        """
        resize_width_ratio = image.width/1000.0
        resize_height_ratio = image.height/1000.0

        enlarged_image = image.resize((int(image.width/level_of_pixelization/(resize_width_ratio)), int(image.height/level_of_pixelization/(resize_height_ratio))))
        resized_image = enlarged_image.resize((int(enlarged_image.width*level_of_pixelization*(resize_width_ratio)), int(enlarged_image.height*level_of_pixelization*(resize_height_ratio))))

        return resized_image

    @staticmethod
    def resize_image_free(image, level_of_pixelization):
        """
        Downscale an image and then upscale the image by the same amount, creating a pixelized effect.
        The amount of pixelization depends on the size of the image input.

        :param image: the image to be resized
        :param level_of_pixelization: the level of pixelization intended (below 20 recommended)
        :type image: an image file
        :type level_of_pixelization: float
        """
        enlarged_image = image.resize((int(image.width/level_of_pixelization), int(image.height/level_of_pixelization)))
        resized_image = enlarged_image.resize((int(enlarged_image.width*level_of_pixelization), int(enlarged_image.height*level_of_pixelization)))

        return resized_image
