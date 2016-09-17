import cv2
from numpy import *

"""
Image Averaging -- Preprocessing technique

Used to:
1) Reduce noise

Requires:
1) List of images (all MUST be the same size)
"""


def compute_average(imlist):
    """
    Compute the average of a list of images
    """
    # Open the first image & make into array of type float
    averageim = array(cv2.imread(imlist[0]), 'f')

    # Sum the additional images
    for imname in imlist[1:]:
        try:
            averageim += array(cv2.imread(imname))
        except:
            print("Could not open " + imname)

    # Computing the average
    averageim /= len(imlist)

    # Returning average
    return averageim

if __name__ == '__main__':
    img_list = ["../images/targets_300.jpg", "../images/targets_400.jpg"]

    cv2.imshow("average", compute_average(img_list) / 255.0)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
