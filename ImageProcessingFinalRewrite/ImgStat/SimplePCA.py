import numpy
import ImageOperation.ImageMath as ImageMath

class SimplePCA:
    
    def __init__(self, data):
        self.covariance_matrix = numpy.cov(data)
        self.eigenvalues, self.eigenvectors = numpy.linalg.eig(self.covariance_matrix)
    
    @classmethod
    def init_with_canny_img(cls, img, image):
        mean_pixel = ImageMath.get_bw_img_mean_pixel(img, image)
        x_vals = []
        y_vals = []
        for x in range(0, img.size[0]):
            for y in range(0, img.size[1]):
                if image[x,y] != 0:
                    x_vals.append(x - mean_pixel[0])
                    y_vals.append(y - mean_pixel[1])
        return SimplePCA(numpy.asarray([x_vals, y_vals]))
    
    def get_covariance_matrix(self):
        return self.covariance_matrix
    
    def get_eigenvalues(self):
        return self.eigenvalues
    
    def get_eigenvectors(self):
        return self.eigenvectors