import cv2
import os
import numpy as np

def run_blob_detection(image):
    detector = cv2.MSER_create(1, 1000, 3000)
    keypoints = detector.detect(image)
    keypoints2 = detector.detect((255-image))

    im_with_keypoints = cv2.drawKeypoints(image, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
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
    number_of_colors = 3

    # Applying kmeans clustering
    ret, label, center = cv2.kmeans(RGB_components, number_of_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    final_img = res.reshape((img.shape))

    cv2.imshow("KMeans", final_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def denoise(im, U_init, tolerance=0.1, tau=0.125, tv_weight=100):
    """
    An implementation of the Rudin-Osher-Fatemi (ROF) denoising model using
    the numerical procedure presented in eq (11) A. Chambolle (2005).

    Input: noisy input image (grayscale), initial guess for I, weight of the
    TV-regularizing term, steplength, tolerance for stop criterion.

    Output: denoised and detextured image, texture residual.
    """
    # Size of noisy image
    m, n = im.shape

    # Initialize
    U = U_init
    Px = im # x-component to the dual field
    Py = im # y-component of the dual field
    error = 1

    while (error > tolerance):
        Uold = U

        # Gradient of primal variable
        GradUx = np.roll(U, -1, axis=1) - U # x-component of U's gradient
        GradUy = np.roll(U, -1, axis=0) - U # y-component of U's gradient

        # Update the dual variable
        PxNew = Px + (tau/tv_weight) * GradUx
        PyNew = Py + (tau/tv_weight) * GradUy
        NormNew = np.maximum(1, np.sqrt(PxNew**2 + PyNew**2))

        Px = PxNew/NormNew # update of x-component (dual)
        Py = PyNew/NormNew # update of y-component (dual)

        # Update the primal variable
        RxPx = np.roll(Px, 1, axis=1) # right x-translation of x-component
        RyPy = np.roll(Py, 1, axis=0) # right y-translation of y-component

        DivP = (Px - RxPx) + (Py - RyPy) # divergence of the dual field

        U = im + tv_weight * DivP # update of the primal variable

        # Update of error
        error = np.linalg.norm(U - Uold) / np.sqrt(n * m)

    # Returning denoised image and textual residual
    return U / 255.0, im - U


if __name__ == '__main__':
    new_path = "/Users/vtolpegin/Desktop/SUAS/Generated Targets BlockText/Images/Generated Target 17.png"
    image = cv2.imread(new_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    denoised_image, _ = denoise(np.array(image), np.array(image))

    cv2.imshow("KMeans", denoised_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    run_blob_detection(denoised_image)#image)
    #run_kmeans(image)
    """
    path = "/Users/vtolpegin/Desktop/SUAS/Generated Targets BlockText/Images/"
    for subdir, dirs, files in os.walk(path):
        for filename in files[1:]:
            filepath = os.path.join(path, filename)
            #print(filepath)
            image = cv2.imread(filepath)

            run_blob_detection(image)
            run_kmeans(image)
    """
