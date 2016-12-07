'''
Created on Nov 29, 2016

@author: phusisian
'''
from PIL import Image

class GrayScale:
    @staticmethod
    def getGrayScaledImage(img, image):
        outputImage = Image.new("RGB", img.size)
        editImage = outputImage.load()
        for x in range(0, outputImage.size[0]):
            for y in range(0, outputImage.size[1]):
                pixelColor = image[x,y]
                grayVal = int(pixelColor[0] * 0.21 + pixelColor[1] * 0.72 + pixelColor[2] * 0.07)
                editImage[x,y] = (grayVal, grayVal, grayVal)
                
        return outputImage