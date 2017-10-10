from PIL import ImageDraw, Image
import abc

class Shape(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, color, rotation):

        """
        :param color: color of shape - RGB
        :type color: 3-tuple
        :param rotation: degrees counterclockwise shape will be rotated
        :type rotation: int
        """

        self.color = color
        self.rotation = rotation

    @abc.abstractmethod
    def get_coordinates(self):
        pass

    @abc.abstractmethod
    def draw(self):
        pass

    def overlay(self, midpoint, image):
        """
        :param midpoint: midpoint where shape will be overlayed on image
        :type midpoint: 2-tuple xy pixel coordinates
        :param image: image for shape to be overlayed on
        :type image: PIL image
        """
        new_shape = self.draw()
        image.paste(new_shape, self.get_upperleft(new_shape, midpoint), new_shape)

    def get_upperleft(self, shape_image, midpoint):
        x1 = midpoint[0]-shape_image.width/2
        y1 = midpoint[1]-shape_image.height/2
        return (x1,y1)
