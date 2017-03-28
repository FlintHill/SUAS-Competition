from math import sqrt

class ColorMath:
    @staticmethod
    def getMagnitudeBetweenColors(color1, color2):
        return sqrt((color2[0]-color1[0])**2 + (color2[1]-color1[1])**2 + (color2[2]-color1[2])**2)

    @staticmethod
    def getMostSimilarColor(colorList, color):
        leastColorDiff = ColorMath.getMagnitudeBetweenColors(color, colorList[0])
        leastColorIndex = 0
        for i in range(1, len(colorList)):
            iterColorDiff = ColorMath.getMagnitudeBetweenColors(color, colorList[i])
            if iterColorDiff < leastColorDiff:
                leastColorDiff = iterColorDiff
                leastColorIndex = i
        return colorList[leastColorIndex]
            