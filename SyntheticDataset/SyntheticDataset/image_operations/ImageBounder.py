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

        leftX = min(list_of_x)
        rightX = max(list_of_x)
        upY = min(list_of_y)
        lowY = max(list_of_y)

        return Rectangle(leftX-1, upY-1, rightX+1, lowY+1)

        """
        dim = img.size
        leftX = dim[0]-1
        rightX = 0
        upY = dim[1]-1
        lowY = 0
        for x in range(0, dim[0]):
            for y in range(0, dim[1]):
                if image[x,y] == color:
                    if x < leftX:
                        leftX = x
                    if x > rightX:
                        rightX = x
                    if y < upY:
                        upY = y
                    if y > lowY:
                        lowY = y
        return Rectangle(leftX-1, upY-1, (rightX+2) - (leftX-1), (lowY+2) - (upY-1))#numbers are being added/subtracted so that the bounds have a margin so that the pixels found aren't cropped out of image
        """
