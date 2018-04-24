from SyntheticDataset.image_operations import Point

class Rectangle(object):

    def __init__(self, xIn, yIn, widthIn, heightIn):
        self.x = xIn
        self.y = yIn
        self.width = widthIn
        self.height = heightIn

    def __repr__(self):
        return "X: " + str(self.x) + " Y: " + str(self.y) + " Width: " + str(self.width) + " Height: " + str(self.height)

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, xIn):
        self.x = xIn

    def setY(self, yIn):
        self.y = yIn

    def getMidpoint(self):
        return Point(self.x + (self.width/2), self.y + (self.height/2))

    def setWidth(self, widthIn):
        self.width = widthIn
    def setHeight(self, heightIn):
        self.height = heightIn

    def fill(self, img, image, color):
        for x in range(self.getX(), self.getX() + self.getWidth()):
            for y in range(self.getY(), self.getY() + self.getHeight()):
                if x < img.size[0] and x >= 0 and y < img.size[1] and y >= 0:
                    image[x,y] = color

    def intersects(self, box):
        """
        Return True if the passed box intersects with this rectangle, False
        otherwise

        :param box: The box to compare intersection with
        :type box: Rectangle
        """
        box_top_left = Point(box.getX(), box.getY())
        box_bottom_left = Point(box.getX(), box.getY() + box.getHeight())
        box_top_right = Point(box.getX() + box.getWidth(), box.getY())
        box_bottom_right = Point(box.getX() + box.getWidth(), box.getY() + box.getHeight())

        if self.contains(box_top_left) or self.contains(box_top_right) or self.contains(box_bottom_left) or self.contains(box_bottom_right):
            return True

        return False

    def contains(self, point):
        return (point.getX() >= self.x and point.getX() <= self.x + self.width and point.getY() >= self.y and point.getY() <= self.y+self.height)
