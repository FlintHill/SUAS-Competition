from random import random
from collections import namedtuple
from SyntheticDataset.color import ColorMath

class ColorList(object):
    colors = []
    namedColors = []
    Color = namedtuple('Color', 'colorName, colorValue', verbose=True)
    '''it'd be better if these used tuples instead since they have to be synced together'''

    def __init__(self):
        '''colors may be adjusted to look more real-world and less intense. Could need some tuning in the future'''
        '''the below DO need to be adjusted, and it is recommended that when creating shapes, that you pull from the RGB
        values directly from this list (e.g. I used (150,0,0) as red, returned brown since at the time, red was (255,0,0)'''

        '''ColorList.namedColors.append(ColorList.Color('black', (20,20,20,255)))
        ColorList.namedColors.append(ColorList.Color('white', (215,215,215,255)))
        ColorList.namedColors.append(ColorList.Color('gray', (128,128,128,255)))
        ColorList.namedColors.append(ColorList.Color('red', (255,0,0,255)))
        ColorList.namedColors.append(ColorList.Color('blue', (0,0,255,255)))
        ColorList.namedColors.append(ColorList.Color('green', (68,180,92,255)))
        ColorList.namedColors.append(ColorList.Color('yellow', (225,225,0,255)))
        ColorList.namedColors.append(ColorList.Color('purple', (128,0,128,255)))
        ColorList.namedColors.append(ColorList.Color('brown', (165,42,42,255)))
        ColorList.namedColors.append(ColorList.Color('orange', (225,165,0,255)))'''


        ColorList.namedColors.append(ColorList.Color('black', (20,20,20,255)))
        ColorList.namedColors.append(ColorList.Color('white', (244,244,252,255)))
        ColorList.namedColors.append(ColorList.Color('gray', (128,128,128,255)))
        ColorList.namedColors.append(ColorList.Color('red', (228, 60, 76,255)))
        ColorList.namedColors.append(ColorList.Color('blue', (44,124,228,255)))
        ColorList.namedColors.append(ColorList.Color('green', (68,180,92,255)))
        ColorList.namedColors.append(ColorList.Color('yellow', (252,220,52,255)))
        ColorList.namedColors.append(ColorList.Color('purple', (116,68,179,255)))
        # Note: Sample targets have a really bad looking brown that seems more orangey
        ColorList.namedColors.append(ColorList.Color('brown', (236,204,132,255)))
        ColorList.namedColors.append(ColorList.Color('orange', (236,132,52,255)))

        ColorList.setUnnamedColors()

    @staticmethod
    def getClosestColorsName(color):
        closestColor = ColorMath.getMostSimilarColor(ColorList.colors, color)
        closestColorIndex = ColorList.colors.index(closestColor)
        return ColorList.namedColors[closestColorIndex][0]

    @staticmethod
    def getColorValueByName(name):
        for i in range(0, len(ColorList.namedColors)):
            if ColorList.namedColors[i][0] == name:
                return ColorList.namedColors[i][1]
        raise ValueError("Color not in list")
        return None

    @staticmethod
    def setUnnamedColors():
        for namedColor in ColorList.namedColors:
            ColorList.colors.append(namedColor[1])

    @staticmethod
    def getRandomColor():
        return ColorList.colors[int(random() * len(ColorList.colors))]

    @staticmethod
    def getRandomColorFromList(colorList):
        return colorList[int(random() * len(colorList))]

    @staticmethod
    def getRandomColorExcludingClosestToBackground(backgroundColor):
        excludeColor = ColorMath.getMostSimilarColor(ColorList.colors, backgroundColor)
        possibleColors = list(ColorList.colors)
        possibleColors.remove(excludeColor)
        return ColorList.getRandomColorFromList(possibleColors)
