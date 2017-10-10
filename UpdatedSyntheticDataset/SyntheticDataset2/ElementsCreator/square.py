from PIL import ImageDraw, Image
from SyntheticDataset2.ElementsCreator import Shape


class Square(Shape):

    def __init__(self, base, color, rotation):
        """
        Initialize a Square shape

        :param base: base in pixels
        :type base: int
        :param color: color of shape - RGB
        :type color: 3-tuple ints
        :param rotation: degrees counterclockwise shape will be rotated
        :type rotation: int
        :param image: image for shape to be overlayed on
        """
        super(Square, self).__init__(color, rotation)
        self.base = base

        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        """
        :param coordinates: drawing coordinates for the shape
        :type coordinates: list of 2-tuple xy pixel coordinates
        """
        return [(0,0), (self.base,self.base)]

    def draw(self):
        new_square = Image.new('RGBA', (self.base,self.base), color=(255,255,255,0))
        draw = ImageDraw.Draw(new_square)
        draw.rectangle(self.coordinates, fill=self.color)
        new_square = new_square.rotate(self.rotation, expand=1)
        return new_square
