from PIL import Image

class BoundedImageCropper(object):
    '''
    Returning a cropped image, in which only the pixels of the intended color remain.
    '''
    @staticmethod
    def cropBoundedImage(image, pixel_data, color):
        dimension = image.size
        list_of_x = []
        list_of_y = []

        for x in range(0, dimension[0]):
            for y in range(0, dimension[1]):
                if  pixel_data[x,y] == color:
                    list_of_x.append(x)
                    list_of_y.append(y)

        leftX = min(list_of_x)
        rightX = max(list_of_x)
        upY = min(list_of_y)
        lowY = max(list_of_y)
        return image.crop((leftX, upY, rightX, lowY))
