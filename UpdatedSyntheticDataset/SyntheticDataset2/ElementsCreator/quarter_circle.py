from PIL import ImageDraw, Image
from SyntheticDataset2.ElementsCreator import Shape


class QuarterCircle(Shape):

    def __init__(self, radius, color, rotation):
        """
        Initialize a Quarter Circle shape

        :param radius: radius in pixels
        :type radius: int
        :param color: color of shape - RGB
        :type color: 3-tuple ints
        :param rotation: degrees counterclockwise shape will be rotated
        :type rotation: int
        """
        super(QuarterCircle, self).__init__(color, rotation)
        self.diameter = radius*2

        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        """
        :param coordinates: drawing coordinates for the shape
        :type coordinates: list of 2-tuple xy pixel coordinates
        """
        return [(0,0), (self.diameter,self.diameter)]

    def draw(self):
        new_quarter_circle = Image.new('RGBA', (self.diameter,self.diameter), color=(255,255,255,0))
        draw = ImageDraw.Draw(new_quarter_circle)
        draw.ellipse(self.coordinates, fill=self.color)
        new_quarter_circle = new_quarter_circle.crop((0,0,self.diameter/2,self.diameter/2))
        new_quarter_circle = new_quarter_circle.rotate(self.rotation, expand=1)
        return new_quarter_circle
