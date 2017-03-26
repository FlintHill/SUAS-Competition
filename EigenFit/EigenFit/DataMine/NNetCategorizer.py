from EigenFit.Vector import *

class NNetCategorizer(object):

    def __init__(self, nnet, eigenvectors, mean, num_dims):
        self.nnet = nnet
        self.mean = mean
        self.eigenvectors = eigenvectors[0: num_dims]
        self.letter_list = map(chr, range(65, 91))

    def get_algorithm_return_smallest_to_large(self, compare_img):
        img_projection = VectorMath.gray_img_to_vector(compare_img)
        projection_weights = EigenProjector.get_projection_weights(img_projection, self.eigenvectors, self.mean)
        nnet_result = self.nnet.get_result(projection_weights)
        outputs = []

        for i in range(0, len(self.letter_list)):
            outputs.append((self.letter_list[i], nnet_result[i], nnet_result[len(nnet_result)-1]))
        sorted_outputs = sorted(outputs, key = lambda output : output[1])
        return sorted_outputs

    def get_algorithm_return_largest_to_small(self, compare_img):
        in_order = self.get_algorithm_return_smallest_to_large(compare_img)
        in_order.reverse()
        return in_order
