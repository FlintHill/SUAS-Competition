'''
Created on Jan 25, 2017

@author: phusisian
'''
class ThreeDDraw:
    Z_SCALE_RATIO = 0.01
    
    @staticmethod
    def getScaledNumber(z, num):
        return int(num + num*z*ThreeDDraw.Z_SCALE_RATIO)