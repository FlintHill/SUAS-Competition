import numpy

def get_set_with_outliers_removed(set, percent_outliers):
    mean = numpy.average(set, axis = 0)
    sorted_by_dist_to_mean = sorted(list(set), key = lambda point : numpy.linalg.norm(numpy.asarray(point) - mean))
    num_to_keep = int((1-percent_outliers)*float(len(set)))
    return numpy.asarray(sorted_by_dist_to_mean[0:num_to_keep])
