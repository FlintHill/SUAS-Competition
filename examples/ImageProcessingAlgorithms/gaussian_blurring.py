import cv2
from scipy.ndimage import filters
from numpy import *

"""
Gaussian Blurring -- Preprocessing technique

Used to:
1) Reduce image noise
2) Reduce details

Requires:
1) Image name
"""


def gaussian_blurring(imname, standard_deviation=5):
    """
    Uses Gaussian blurring to blur an image
    """
    # Loading the image
    im = cv2.imread(imname)

    # Filtering the image
    filtered = zeros(im.shape)
    for i in range(3):
        filtered[:,:,i] = filters.gaussian_filter(im[:,:,i], standard_deviation)

    # Cleaning the data up
    filtered = uint8(filtered)

    # Returning the filtered image
    return filtered

if __name__ == '__main__':
    imname = "../images/IMG_0147.jpg"

    cv2.imshow("filtered", gaussian_blurring(imname))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
