import numpy

class SimplePCA(object):
    """
    Adapted from ImgProcessingCLI's ImgProcessingCLI.ImgStat by Peter Husisian
    """
    def __init__(self, data):
        self.covariance_matrix = numpy.cov(data)
        self.eigenvalues, self.eigenvectors = numpy.linalg.eig(self.covariance_matrix)
        self.sort_eigenvectors_and_eigenvalues()

    @classmethod
    def init_with_monochrome_img(cls, img):
        image = img.load()
        mean_pixel = (0,0)
        x_vals = []
        y_vals = []
        for x in range(0, img.size[0]):
            for y in range(0, img.size[1]):
                if image[x,y] != 0:
                    x_vals.append(x - mean_pixel[0])
                    y_vals.append(y - mean_pixel[1])
        return SimplePCA(numpy.asarray([x_vals, y_vals]))

    def sort_eigenvectors_and_eigenvalues(self):
        eigen_pairs = [(self.eigenvectors[i], self.eigenvalues[i]) for i in range(0, self.eigenvectors.shape[0])]
        eigen_pairs = sorted(eigen_pairs, key = lambda eigen_pair : eigen_pair[1], reverse=True)
        for i in range(0, len(eigen_pairs)):
            self.eigenvalues[i] = eigen_pairs[i][1]
            self.eigenvectors[i] = eigen_pairs[i][0]

    def get_covariance_matrix(self):
        return self.covariance_matrix

    def get_eigenvalues(self):
        return self.eigenvalues

    def get_eigenvectors(self):
        return self.eigenvectors
