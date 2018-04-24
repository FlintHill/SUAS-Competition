class ImageCropper(object):
    '''method could be useless, would prefer to implement python
    special method for a rectangle so I could plug it into the
    tuple portion of the crop function'''

    @staticmethod
    def cropImgToRect(img, cropRect):
        return img.crop((cropRect.getX(), cropRect.getY(), cropRect.getWidth()+cropRect.getX(), cropRect.getHeight()+cropRect.getY()))
