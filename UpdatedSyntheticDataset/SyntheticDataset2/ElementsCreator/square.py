from PIL import ImageDraw, Image


class Square(object):

    def __init__(self, base, color, midpoint, rotation, image):
        """
        Initialize a Square shape

        :param base: base in pixels
        :type base: int
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
        self.color = color
        self.midpoint = midpoint
        self.rotation = rotation
        self.image = image
        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        return [(0,0), (self.base,self.base)]

    def draw(self):
        new_square = Image.new('RGBA', (self.base,self.base), color=(255,255,255,0))
        draw = ImageDraw.Draw(new_square)
        draw.rectangle(self.coordinates, fill=self.color)
        new_square = new_square.rotate(self.rotation, expand=1)
        return new_square

    def overlay(self):
        new_square = self.draw()
        self.image.paste(new_square, self.get_upperleft(new_square), new_square)

    def get_upperleft(self, shape_image):
        x1 = self.midpoint[0]-shape_image.width/2
        y1 = self.midpoint[1]-shape_image.height/2
        return (x1,y1)
