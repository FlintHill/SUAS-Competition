from PIL import ImageDraw, Image
from SyntheticDataset2.ElementsCreator import Shape


class Circle(Shape):

    def __init__(self, radius, color):
        """
        Initialize a Circle shape

        :param radius: radius in pixels
        :type radius: int
        :param color: color of shape - RGB
        :type color: 3-tuple ints
        """
        super(Circle, self).__init__(color, 0)
        self.diameter = radius*2

        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        """
        :param coordinates: drawing coordinates for the shape
        :type coordinates: list of 2-tuple xy pixel coordinates
        """
        return [(0,0), (self.diameter,self.diameter)]

    def draw(self):
        new_circle = Image.new('RGBA', (self.diameter,self.diameter), color=(255,255,255,0))
        draw = ImageDraw.Draw(new_circle)
        draw.ellipse(self.coordinates, fill=self.color)
        return new_circle
