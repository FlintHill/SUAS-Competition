from PIL import ImageDraw, Image
from SyntheticDataset2.ElementsCreator import Shape

class Cross(Shape):

    def __init__(self, height, color, rotation):
        """
        Initialize a Cross shape

        :param height: height in pixels
        :type height: int
        :param color: color of shape - RGB
        :type color: 3-tuple int
        :param rotation: degrees counterclockwise shape will be rotated
        :type rotation: int
        """
        super(Cross, self).__init__(color, rotation)
        self.height = height

        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        """
        :param coordinates: drawing coordinates for the shape
        :type coordinates: list of 2-tuple xy pixel coordinates
        """
        x1 = self.height/3
        y1 = 0
        x2 = 2*self.height/3
        y2 = 0
        x3 = 2*self.height/3
        y3 = self.height/3
        x4 = self.height
        y4 = self.height/3
        x5 = self.height
        y5 = 2*self.height/3
        x6 = 2*self.height/3
        y6 = 2*self.height/3
        x7 = 2*self.height/3
        y7 = self.height
        x8 = self.height/3
        y8 = self.height
        x9 = self.height/3
        y9 = 2*self.height/3
        x10 = 0
        y10 = 2*self.height/3
        x11 = 0
        y11 = self.height/3
        x12 = self.height/3
        y12 = self.height/3

        return [(x1,y1),(x2,y2),(x3,y3),(x4,y4),(x5,y5),(x6,y6),(x7,y7),(x8,y8),(x9,y9),(x10,y10),(x11,y11),(x12,y12)]

    def draw(self):
        new_cross = Image.new('RGBA', (self.height,self.height), color=(255,255,255,0))
        draw = ImageDraw.Draw(new_cross)
        draw.polygon(self.coordinates, fill=self.color)
        new_cross = new_cross.rotate(self.rotation, expand=1)
        return new_cross
