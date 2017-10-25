from PIL import Image
import random, os

class BackgroundGenerator(object):

    def __init__(self,path_to_backrounds):
        """
        Create a background for a Target or TargetField

        :param path_to_backgrounds: location of backgrounds directory on computer
        """
        self.path_to_backgrounds = path_to_backgrounds

    def generate_full_background(self):
        """
        Return a full sized background
        """
        image_list = os.listdir(self.path_to_backrounds)
        image_list = [f for f in image_list if not f.startswith(".")]

        background = Image.open(self.path_to_backrounds + "/" + random.choice(image_list))
        return background

    def generate_specific_background(self,specified_width,specified_height):
        """
        Return a background with a specified size

        :param width: width of background in pixels
        :type width: int
        :param height: height of background in pixels
        :type height: int
        """
        background = self.generate_full_background()
        crop_coordinates = self.get_random_coordinates(background.width,background.height,specified_width,specified_height)
        background = background.crop(crop_coordinates)
        return background

    def get_random_coordinates(self,background_width,background_height,specified_width,specified_height):
        x1 = random.randint(0,background_width-specified_width)
        y1 = random.randint(0,background_height-specified_height)
        x2 = x1+specified_width
        y2 = y1+specified_height
        return (x1,y1,x2,y2)
