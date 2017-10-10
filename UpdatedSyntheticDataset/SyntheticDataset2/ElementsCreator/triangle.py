from PIL import ImageDraw, Image
from SyntheticDataset2.ElementsCreator import Shape


class Triangle(Shape):

    def __init__(self, base, height, color, rotation):
        """
        Initialize a Triangle shape

        :param base: base in pixels
        :type base: int
        :param height: height in pixels
        :type hight: int
        :param color: color of shape - RGB
        :type color: 3-tuple ints
        :param rotation: degrees counterclockwise shape will be rotated
        :type rotation: int
        """
        super(Triangle, self).__init__(color, rotation)
        self.base = base
        self.height = height

        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        """
        :param coordinates: drawing coordinates for the shape
        :type coordinates: list of 2-tuple xy pixel coordinates
        """
        x1=self.base/2
        y1=0
        x2=0
        y2=self.height
        x3=self.base
        y3=self.height
        return [(x1,y1), (x2,y2), (x3,y3)]

    def draw(self):
        new_triangle = Image.new('RGBA', (self.base, self.height), color=(255,255,255,0))
        draw = ImageDraw.Draw(new_triangle)
        draw.polygon(self.coordinates, fill=self.color)
        new_triangle = new_triangle.rotate(self.rotation, expand=1)
        return new_triangle
