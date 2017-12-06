from PIL import ImageDraw, Image
from SyntheticDataset2.ElementsCreator import Shape


class HalfCircle(Shape):

    def __init__(self, radius, color, rotation):
        """
        Initialize a Half Circle shape

        :param radius: radius in pixels
        :type radius: int
        :param color: color of shape - RGB
        :type color: 3-tuple ints
        :param rotation: degrees counterclockwise shape will be rotated
        :type rotation: int
        """
        super(HalfCircle, self).__init__(color, rotation)
        self.diameter = radius*2

        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        """
        :param coordinates: drawing coordinates for the shape
        :type coordinates: list of 2-tuple xy pixel coordinates
        """
        return [(0,0), (self.diameter,self.diameter)]

    def draw(self):
        new_half_circle = Image.new('RGBA', (self.diameter,self.diameter/2), color=(255,255,255,0))
        draw = ImageDraw.Draw(new_half_circle)
        draw.ellipse(self.coordinates, fill=self.color)
        new_half_circle = new_half_circle.crop((0,0,self.diameter,self.diameter/2))
        new_half_circle = new_half_circle.rotate(self.rotation, expand=1)
        return new_half_circle
