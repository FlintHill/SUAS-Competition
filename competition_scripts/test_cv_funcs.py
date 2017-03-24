import cv2
import numpy as np

def run_blob_detection(image):
    detector = cv2.MSER_create(1, 3000, 30000)
    keypoints = detector.detect(image)
    keypoints2 = detector.detect((255-image))

    im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    im_with_keypoints = cv2.drawKeypoints(im_with_keypoints, keypoints2, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    cv2.imshow("Blobs", im_with_keypoints)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def run_kmeans(img):
    """
    Simplifies the image's number of colors by applying K-Means clustering for
    color quantization.
    """
    # @TODO: Add option to configure settings (kwargs passed to method?)

    # Separating RGB components of image
    RGB_components = img.reshape((-1,3))
    RGB_components = np.float32(RGB_components)

    # Creating settings for kmeans clustering
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    number_of_colors = num_colors

    # Applying kmeans clustering
    ret, label, center = cv2.kmeans(RGB_components, 3, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    final_img = res.reshape((img.shape))

    cv2.imshow("KMeans", final_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    image_filename = "..."
    image = cv2.imread(filename)

    run_blob_detection(image)
    run_kmeans(image)
