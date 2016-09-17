import cv2
from numpy import *

"""
Histogram Equalization -- Preprocessing technique

Used to:
1) Normalize image intensity
2) Improve contrast

Requires:
1) Grayscale image
"""


def histeq(im, nbr_bins=1024):
    """
    Histogram equalization of a grayscale image
    """
    # Get Histogram
    imhist, bins = histogram(im.flatten(), nbr_bins, normed=True)
    cdf = imhist.cumsum() # Cumulative distribution function
    cdf = 255 * cdf / cdf[-1] # Normalize

    # Use linear interpolation of cdf to find new pixel values
    im2 = interp(im.flatten(), bins[:-1], cdf)

    # Return the new image
    return im2.reshape(im.shape), cdf

# Testing histogram equalization
if __name__ == '__main__':
    im = array(cv2.cvtColor(cv2.imread("../images/targets_300.jpg"), cv2.COLOR_BGR2GRAY))
    im2, cdf = histeq(im)

    cv2.imshow("im2", im2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
