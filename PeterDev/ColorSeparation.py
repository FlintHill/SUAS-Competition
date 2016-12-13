'''
Created on Dec 2, 2016

@author: phusisian
'''

from root.nested.ColorLayer import ColorLayer
from root.nested.ColorLayers import ColorLayers
from PIL import Image

class ColorSeparation:
    
    #sticking it here seems like it could be more functional in the ColorLayers class itself.
    @staticmethod
    def getColorLayers(img, image):
        dim = img.size
        colorLayers = ColorLayers(img, image)
        for x in range(0, dim[0]):
            for y in range(0, dim[1]):
                if image[x,y] != (0,0,0):
                    index = colorLayers.getIndexOfColor(image[x,y])
                    if index >= 0:
                        colorLayers[index].drawPixel(image[x,y], x, y)
                    else:
                        colorLayers.append(ColorLayer.initWithoutImg(dim, image[x,y], x, y))
        return colorLayers