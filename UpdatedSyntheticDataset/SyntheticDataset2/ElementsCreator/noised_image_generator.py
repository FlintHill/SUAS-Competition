from SyntheticDataset2.ImageOperations.image_extender import ImageExtender
from SyntheticDataset2.ImageOperations.gaussian_noise_generator import GaussianNoiseGenerator
from SyntheticDataset2.ImageOperations.bounded_image_cropper import BoundedImageCropper

class NoisedImageGenerator(object):

    @staticmethod
    def generate_noised_image_by_level(image, level):
        """
        Blur an image with the intended noise level
        :param image: the image to modify
        :param level: the level of the noise (more explanation in gaussian_noise_generator)
        :type image: an image file
        :type level: int (preferably from 0 to 100)
        """
        image1 = ImageExtender.extend_image(image, int(image.width), int(image.height))
        image2 = GaussianNoiseGenerator.generate_gaussian_noise_by_level(image1, level, image.width)
        return BoundedImageCropper.crop_bounded_image_inverse(image2, image2.load(), (255,255,255,0))

    @staticmethod
    def generate_noised_image_by_radius(image, radius):
        """
        Blur an image with the intended radius
        :param image: the image to modify
        :param level: the radius of the noise
        :type image: an image file
        :type radius: int (representing pixels)
        """
        image1 = ImageExtender.extend_image(image, int(image.width), int(image.height))
        image2 = GaussianNoiseGenerator.generate_gaussian_noise_by_radius(image1, radius)
        return BoundedImageCropper.crop_bounded_image_inverse(image2, image2.load(), (255,255,255,0))
