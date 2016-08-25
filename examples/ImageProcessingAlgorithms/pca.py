import cv2
import PIL
from numpy import *

"""
PCA (Principal Component Analysis) -- Preprocessing technique

Used for:
1) Dimensionality reduction

Requires:
1) Matrix with training data stored as flattened [numpy] arrays in rows

Returns:
1) Projection matrix (with important dimensions first)
2) Variance
3) Mean
"""


def pca(input_matrix):
    """
    Principal Component Analysis for dimensionality reduction
    """
    # Get dimensions
    num_data, dim = input_matrix.shape

    # Center data
    mean_input_matrix = input_matrix.mean(axis=0)
    input_matrix = input_matrix - mean_input_matrix

    if dim > num_data:
        # PCA - compact trick used
        M = dot(input_matrix, input_matrix.T) # Convariance matrix
        e, EV = linalg.eigh(M) # eigenvalues and eigenvectors
        tmp = dot(input_matrix.T, EV) # this is the compact trick
        V = tmp[::-1] # reverse since the last eigenvectors are the ones we want
        S = sqrt(e)[::-1] # reverse since eigenvalues are in increasing order
        for i in range(V.shape[1]):
            V[:,i] /= S
    else:
        # PCA - SVD used
        U, S, V = linalg.sv(input_matrix)
        V = V[:num_data] # only makes sense to return the first num_data

    # Return the projection matrix, the variance, and the mean
    return V, S, mean_input_matrix

if __name__ == '__main__':
    # @TODO add example code to test here
    pass
