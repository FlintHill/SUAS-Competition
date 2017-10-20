from PIL import Image
import random
import os

class BackgroundGenerator(object):

    def __init__(self,width,height,path_to_backrounds):
        """
        Return a background for a Target

        :param width: width of background
        :type width: int
        :param height: height of background
        :type height: int
        :param path_to_backrounds: location of backgrounds directory on computer
        """
        self.width=width
        self.height=height
        self.path_to_backrounds=path_to_backrounds

    def generate_background(self):
        try:
            os.remove(self.path_to_backrounds + "/.DS_Store")
        except:
            pass
        background = Image.open(self.path_to_backrounds + "/" + random.choice(os.listdir(self.path_to_backrounds)))
        crop_coordinates = self.get_random_coordinates(background.width,background.height)
        background = background.crop(crop_coordinates)
        return background

    def get_random_coordinates(self,background_width,background_height):
        x1 = random.randint(0,background_width-self.width)
        y1 = random.randint(0,background_height-self.height)
        x2 = x1+self.width
        y2 = y1+self.height
        return (x1,y1,x2,y2)
