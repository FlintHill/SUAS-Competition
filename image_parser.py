__author__ = 'Vale Tolpegin'

import numpy as np
import cv2

class image_parser:
    def __init__( self, *args, **kwargs ):
        pass

    def parse( picture_file_name ):
        #set image variable here with the image file picture_file

        #find shapes in image ( basic geometric shapes such as circles, squares, triangles, etc )

        #inside of those geometric shapes, find the number of different colors
        #if there are 2 colors ( other than black, no more and no less )
            #if there are 2 distinct seperate colors ( other than black ) within a couple of pixels of each other
                #compare the ratio of those 2 colors ( non black )
                #if that ratio is close to 2:1 ( shape:letter )
                    #return True

        return false

if __name__ == '__main__':
    pass