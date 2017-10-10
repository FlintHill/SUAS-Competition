from PIL import ImageDraw, Image
from SyntheticDataset2.ElementsCreator import Shape


class Rectangle(Shape):

    def __init__(self, width, height, color, rotation):
        """
        Initialize a Rectangle shape

        :param width: width in pixels
        :type width: int
        :param height: height in pixels
        :type hight: int
        :param color: color of shape - RGB
        :type color: 3-tuple ints
        :param rotation: degrees counterclockwise shape will be rotated
        :type rotation: int
        """
        super(Rectangle, self).__init__(color, rotation)
        self.width = width
        self.height = height

        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        """
        :param coordinates: drawing coordinates for the shape
        :type coordinates: list of 2-tuple xy pixel coordinates
        """
        return [(0,0), (self.width,self.height)]

    def draw(self):
        new_rectangle = Image.new('RGBA', (self.width,self.height), color=(255,255,255,0))
        draw = ImageDraw.Draw(new_rectangle)
        draw.rectangle(self.coordinates, fill=self.color)
        new_rectangle = new_rectangle.rotate(self.rotation, expand=1)
        return new_rectangle
