from PIL import ImageDraw, Image


class Rectangle(object):

    def __init__(self, width, height, color, midpoint, rotation, image):
        """
        Initialize a Rectangle shape

        :param width: width in pixels
        :type width: int
        :param height: height in pixels
        :type hight: int
        :param color: color of shape - RGB
        :type color: 3-tuple
        :param midpoint: midpoint where shape will be overlayed on image
        :type midpoint: 2-tuple xy pixel coordinates
        :param rotation: degrees counterclockwise shape will be rotated
        :type rotation: int
        :param image: image for shape to be overlayed on
        :type image: PIL image

        :param coordinates: drawing coordinates for the shape
        :type coordinates: list of 2-tuple xy pixel coordinates
        """

        self.width = width
        self.height = height
        self.color = color
        self.midpoint = midpoint
        self.rotation = rotation
        self.image = image
        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        return [(0,0), (self.width,self.height)]

    def draw(self):
        new_rectangle = Image.new('RGBA', (self.width,self.height), color=(255,255,255,0))
        draw = ImageDraw.Draw(new_rectangle)
        draw.rectangle(self.coordinates, fill=self.color)
        new_rectangle = new_rectangle.rotate(self.rotation, expand=1)
        return new_rectangle

    def overlay(self):
        new_rectangle = self.draw()
        self.image.paste(new_rectangle, self.get_upperleft(new_rectangle), new_rectangle)

    def get_upperleft(self, shape_image):
        x1 = self.midpoint[0]-shape_image.width/2
        y1 = self.midpoint[1]-shape_image.height/2
        return (x1,y1)
