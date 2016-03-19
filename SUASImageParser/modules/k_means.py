import cv2
import numpy as np

def simplify_by_k_means(img, num_colors=3):
    """
    Simplifies the image's number of colors by applying K-Means clustering for
    color quantization.
    """
    # @TODO: Add option to configure settigns (kwargs passed to method?)

    # Separating RGB components of image
    RGB_components = img.reshape((-1,3))
    RGB_components = np.float32(RGB_components)

    # Creating settings for kmeans clustering
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    number_of_colors = num_colors

    # Applying kmeans clustering
    ret, label, center = cv2.kmeans(RGB_components, number_of_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    final_img = res.reshape((img.shape))

    # Returning the final image
    return final_img
