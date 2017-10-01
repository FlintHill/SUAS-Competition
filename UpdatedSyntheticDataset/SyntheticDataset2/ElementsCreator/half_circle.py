from PIL import ImageDraw, Image


class HalfCircle(object):

    def __init__(self, radius, color, midpoint, rotation, image):
        """
        Initialize a Half Circle shape

        :param radius: radius in pixels
        :type radius: int
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

        self.diameter = radius*2
        self.color = color
        self.midpoint = midpoint
        self.rotation = rotation
        self.image = image
        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        return [(0,0), (self.diameter,self.diameter)]

    def draw(self):
        new_half_circle = Image.new('RGBA', (self.diameter,self.diameter/2), color=(255,255,255,0))
        draw = ImageDraw.Draw(new_half_circle)
        draw.ellipse(self.coordinates, fill=self.color)
        new_half_circle = new_half_circle.crop((0,0,self.diameter,self.diameter/2))
        new_half_circle = new_half_circle.rotate(self.rotation, expand=1)
        return new_half_circle

    def overlay(self):
        new_half_circle = self.draw()
        self.image.paste(new_half_circle, self.get_upperleft(new_half_circle), new_half_circle)

    def get_upperleft(self, shape_image):
        x1 = self.midpoint[0]-shape_image.width/2
        y1 = self.midpoint[1]-shape_image.height/2
        return (x1,y1)
