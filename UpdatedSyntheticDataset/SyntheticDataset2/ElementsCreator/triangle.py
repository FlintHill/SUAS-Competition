from PIL import ImageDraw, Image


class Triangle(object):

    def __init__(self, base, height, color, midpoint, rotation, image):
        """
        Initialize a Triangle shape

        :param base: base in pixels
        :type base: int
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

        self.base = base
        self.height = height
        self.color = color
        self.midpoint = midpoint
        self.rotation = rotation
        self.image = image
        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
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

    def overlay(self):
        new_triangle = self.draw()
        self.image.paste(new_triangle, self.get_upperleft(new_triangle), new_triangle)

    def get_upperleft(self, shape_image):
        x1 = self.midpoint[0]-shape_image.width/2
        y1 = self.midpoint[1]-shape_image.height/2
        return (x1,y1)
