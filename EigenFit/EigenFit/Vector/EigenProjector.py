import numpy

def get_projection_weights(img_vector, eigenvectors, mean_vector):
    mean_adjusted_img_vector = img_vector - mean_vector
    
    weights = numpy.zeros((eigenvectors.shape[0]))
    for i in range(0, weights.shape[0]):
        weights[i] = numpy.dot(mean_adjusted_img_vector, eigenvectors[i])
    return weights

def get_reconstruction_img_vector(projection_weights, eigenvectors):
    reconstruction_vector = numpy.zeros((eigenvectors.shape[1]))
    for i in range(0, projection_weights.shape[0]):
        reconstruction_vector = numpy.add(reconstruction_vector, eigenvectors[i] * projection_weights[i])
    return reconstruction_vector