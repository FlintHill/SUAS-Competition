import cv2
from numpy import *
import gaussian_blurring

"""
Denoising of images using the ROF (Rudin-Osher-Fatemi) de-noising model

Used to:
1) Remove noise in images

Requires:
1) Grayscale image
"""


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
        GradUx = roll(U, -1, axis=1) - U # x-component of U's gradient
        GradUy = roll(U, -1, axis=0) - U # y-component of U's gradient

        # Update the dual variable
        PxNew = Px + (tau/tv_weight) * GradUx
        PyNew = Py + (tau/tv_weight) * GradUy
        NormNew = maximum(1, sqrt(PxNew**2 + PyNew**2))

        Px = PxNew/NormNew # update of x-component (dual)
        Py = PyNew/NormNew # update of y-component (dual)

        # Update the primal variable
        RxPx = roll(Px, 1, axis=1) # right x-translation of x-component
        RyPy = roll(Py, 1, axis=0) # right y-translation of y-component

        DivP = (Px - RxPx) + (Py - RyPy) # divergence of the dual field

        U = im + tv_weight * DivP # update of the primal variable

        # Update of error
        error = linalg.norm(U - Uold) / sqrt(n * m)

    # Returning denoised image and textual residual
    return U / 255.0, im - U

if __name__ == '__main__':
    imname = "../images/IMG_0150.jpg"
    blurred = cv2.cvtColor(gaussian_blurring.gaussian_blurring(imname, 10), cv2.COLOR_BGR2GRAY)

    cv2.imshow("blurred", blurred)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    U, T = denoise(array(blurred), array(blurred))

    cv2.imshow("denoised", U / 255.0)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
