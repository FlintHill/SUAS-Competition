from SyntheticDataset.image_operations import Rectangle

class ImageBounder(object):
    '''returns the bounds of a color in the image (with a margin so the pixel it finds at the edge is not excluded)'''

    @staticmethod
    def getBoundsOfColor(img, image, color):
        dim = img.size
        list_of_x = []
        list_of_y = []

        for x in range(0, dim[0]):
            for y in range(0, dim[1]):
                if  image[x,y] == color:
                    list_of_x.append(x)
                    list_of_y.append(y)

        leftX = min(list_of_x)-1
        rightX = max(list_of_x)+2
        upY = min(list_of_y)-1
        lowY = max(list_of_y)+2

        return Rectangle(leftX, upY, rightX-leftX, lowY-upY)
