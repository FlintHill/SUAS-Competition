from PIL import ImageDraw, Image
from SyntheticDataset2.ElementsCreator import Shape


class Trapezoid(Shape):

    def __init__(self, base1, base2, height, color, rotation):
        """
        Initialize a Trapezoid shape

        :param base1: base1 in pixels
        :type base1: int
        :param base2: base2 in pixels
        :type base2: int
        :param base2: height in pixels
        :type base2: int
        :param color: color of shape - RGB
        :type color: 3-tuple ints
        :param rotation: degrees counterclockwise shape will be rotated
        :type rotation: int
        """
        super(Trapezoid, self).__init__(color, rotation)
        self.base1 = base1
        self.base2 = base2
        self.height = height

        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        """
        :param coordinates: drawing coordinates for the shape
        :type coordinates: list of 2-tuple xy pixel coordinates
        """
        if self.base2 > self.base1:
            x1=(self.base2-self.base1)/2
            y1=0
            x2=(self.base2-self.base1)/2 + self.base1
            y2=0
            x3=self.base2
            y3=self.height
            x4=0
            y4=self.height

        if self.base1 > self.base2:
            x1=0
            y1=0
            x2=self.base1
            y2=0
            x3=(self.base1-self.base2)/2 + self.base2
            y3=self.height
            x4=(self.base1-self.base2)/2
            y4=self.height

        return [(x1,y1),(x2,y2),(x3,y3),(x4,y4)]

    def draw(self):
        if self.base2 > self.base1:
            new_trap = Image.new('RGBA', (self.base2,self.height), color=(255,255,255,0))
        if self.base1 > self.base2:
            new_trap = Image.new('RGBA', (self.base1,self.height), color=(255,255,255,0))
        draw = ImageDraw.Draw(new_trap)
        draw.polygon(self.coordinates, fill=self.color)
        new_trap = new_trap.rotate(self.rotation, expand=1)
        return new_trap
