from PIL import ImageDraw, Image


class Trapezoid(object):

    def __init__(self, base1, base2, height, color, midpoint, rotation, image):
        """
        Initialize a Trapezoid shape

        :param base1: base1 in pixels
        :type base1: int
        :param base2: base2 in pixels
        :type base2: int
        :param base2: height in pixels
        :type base2: int
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

        self.base1 = base1
        self.base2 = base2
        self.height = height
        self.color = color
        self.midpoint = midpoint
        self.rotation = rotation
        self.image = image
        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
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

    def overlay(self):
        new_trap = self.draw()
        self.image.paste(new_trap, self.get_upperleft(new_trap), new_trap)

    def get_upperleft(self, shape_image):
        x1 = self.midpoint[0]-shape_image.width/2
        y1 = self.midpoint[1]-shape_image.height/2
        return (x1,y1)
