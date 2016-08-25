import cv2
from scipy.ndimage import filters
from numpy import *

"""
Sobel & Gaussian X and Y derivative identification -- Preprocessing technique

Used to:
1) Identify gradient magnitude
2) Noise reduction

Requires:
1) Grayscale image
"""


def sobel_xy_derivative(img):
    """
    Applies Sobel filters to identify X and Y derivatives
    """
    # Sobel derivative filters
    imx = zeros(img.shape)
    filters.sobel(img, 1, imx)

    imy = zeros(img.shape)
    filters.sobel(img, 0, imy)

    magnitude = sqrt(imx**2 + imy**2)

    # Returning the filtered image
    return magnitude

def gaussian_xy_derivatives(img, standard_deviation=5):
    """
    Applies Gaussian filters to identify the X and Y derivatives
    """
    # Gaussian derivative filters
    imx = zeros(img.shape)
    filters.gaussian_filter(img, (standard_deviation, standard_deviation), (0,1), imx)

    imy = zeros(img.shape)
    filters.sobel(img, (standard_deviation, standard_deviation), (1,0), imx)

    magnitude = sqrt(imx**2 + imy**2)

    # Returning the filtered image
    return magnitude

if __name__ == '__main__':
    img = cv2.imread("../images/IMG_0147.jpg")

    cv2.imshow("sobel filtered", sobel_xy_derivative(img))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imshow("gaussian filtered", gaussian_xy_derivatives(img))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
