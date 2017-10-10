from PIL import ImageFilter

class GaussianNoiseGenerator(object):

    @staticmethod
    def generate_gaussian_noise_by_level(image, level, width):
        """
        Add Gaussian noise of an intended level to an image.
        :param image: an image input
        :param level: represent the percentage of blur. (Ex: level 1 means that the
                      image is blurred with the radius of 0.5 percent of its width.)
        :param width: the width that the level refers to. Input image.width if its
                      width is to be the benchmark. And specify otherwise if not.
        :type image: an image file
        :type level: a float from 0.0 to 100.0
        :type width: int (representing pixels)
        """
        return image.filter(ImageFilter.GaussianBlur(radius = int(width*level/200)))

    @staticmethod
    def generate_gaussian_noise_by_radius(image, radius):
        """
        Add Gaussian noise of an intended radius to an image
        :param image: an image input
        :param radius: the radius of the blur
        :type image: an image file
        :type radius: int (representing pixel)
        """
        return image.filter(ImageFilter.GaussianBlur(radius = radius))
