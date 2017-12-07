from PIL import ImageDraw, Image
from SyntheticDataset2.ElementsCreator import Shape
import math

class Heptagon(Shape):

    def __init__(self, radius, color, rotation):
        """
        Initialize a Heptagon shape

        :param radius: radius in pixels
        :type radius: int
        :param color: color of shape - RGB
        :type color: 3-tuple
        :param rotation: degrees counterclockwise shape will be rotated
        :type rotation: int
        """
        super(Heptagon, self).__init__(color, rotation)
        self.radius = radius

        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        """
        :param coordinates: drawing coordinates for the shape
        :type coordinates: list of 2-tuple xy pixel coordinates
        """
        x1 = self.radius*math.cos(math.radians(38-(360/7)*0))+self.radius
        y1 = self.radius*math.sin(math.radians(38-(360/7)*0))+self.radius
        x2 = self.radius*math.cos(math.radians(38-(360/7)*1))+self.radius
        y2 = self.radius*math.sin(math.radians(38-(360/7)*1))+self.radius
        x3 = self.radius*math.cos(math.radians(38-(360/7)*2))+self.radius
        y3 = self.radius*math.sin(math.radians(38-(360/7)*2))+self.radius
        x4 = self.radius*math.cos(math.radians(38-(360/7)*3))+self.radius
        y4 = self.radius*math.sin(math.radians(38-(360/7)*3))+self.radius
        x5 = self.radius*math.cos(math.radians(38-(360/7)*4))+self.radius
        y5 = self.radius*math.sin(math.radians(38-(360/7)*4))+self.radius
        x6 = self.radius*math.cos(math.radians(38-(360/7)*5))+self.radius
        y6 = self.radius*math.sin(math.radians(38-(360/7)*5))+self.radius
        x7 = self.radius*math.cos(math.radians(38-(360/7)*6))+self.radius
        y7 = self.radius*math.sin(math.radians(38-(360/7)*6))+self.radius

        return [(x1,y1),(x2,y2),(x3,y3),(x4,y4),(x5,y5),(x6,y6),(x7,y7)]

    def draw(self):
        new_heptagon = Image.new('RGBA', (2*self.radius,2*self.radius), color=(255,255,255,0))
        draw = ImageDraw.Draw(new_heptagon)
        draw.polygon(self.coordinates, fill=self.color)
        new_heptagon = new_heptagon.rotate(self.rotation, expand=1)
        return new_heptagon
