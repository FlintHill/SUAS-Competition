import ImgProcessingCLI.Array.ArrayHelper as ArrayHelper
import numpy
from sklearn.decomposition import PCA
import scipy
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from math import sqrt, pi, exp

BINS = 100#100
SMOOTH_WINDOW = 25#20#50
DIR_SMOOTH_WINDOW = 10
'''was trained using many generated images to find a good split value
normal distribution differences below this are false positives (contain no targets)
and values above this are targets'''
NORMAL_DISTRIBUTION_DIFFERENCE_SPLIT_VAL = 1.8900099746257205e-05

'''the below are the most suited to optimization -- especially probability density threshold'''

'''the minimum number of maxima for the target to be classified as not a false positive
'''
NUM_MAXES_THRESHOLD = 1
'''must be a value between 0 and 1'''
PROBABILITY_DENSITY_THRESHOLD = .12#0
#MIN_DISTRIBUTION_PEAK = 0
MIN_IHIST_DIR_VAL = .00002


def get_if_is_false_positive(img, image, show = False):
    rgbs = get_rgbs(img, image)
    mean_rgb = get_mean_rgb(rgbs)
    eigenvectors = get_eigenvectors(rgbs, mean_rgb)
    i_projections = get_i_projections(rgbs, mean_rgb, eigenvectors)
    i_hist = get_i_projections_histogram(i_projections)


    i_hist_dir = ArrayHelper.mean_smooth(numpy.gradient(i_hist), 15)
    dir_roots  = ArrayHelper.get_root_locations(i_hist_dir)
    maxes = ArrayHelper.get_maxes_from_deriv(i_hist_dir)
    mins = ArrayHelper.get_mins_from_deriv(i_hist_dir)
    mins = list(mins)
    mins.insert(0, 0)
    mins.append(i_hist.shape[0])
    mins = numpy.asarray(mins)

    normal_dist = get_normal_distribution_estimation(i_hist, i_projections)
    normal_dist_density = scipy.integrate.cumtrapz(normal_dist)

    if show:
        plt.clf()
        plt.plot(i_hist)
        plt.plot(normal_dist, color = 'green')
        plt.plot(numpy.sqrt(numpy.abs(i_hist - normal_dist)), color = 'red')
        plt.axvline(0)
        plt.axhline(0)
        plt.show()


    num_thresholded_maxes = 0
    avg_squared_diff = get_avg_squared_histogram_difference(i_hist, normal_dist)
    '''would probably be best if this were a decision tree'''
    '''if dir_roots.shape[0] > 2 and avg_squared_diff > 1.0 * 10.0 ** -6:
        return False'''
    if avg_squared_diff > NORMAL_DISTRIBUTION_DIFFERENCE_SPLIT_VAL:
        return False

    return True

def get_rgbs(img, image):
    rgbs = []
    for x in range(0, img.size[0]):
        for y in range(0, img.size[1]):
            rgbs.append(numpy.asarray(image[x,y][0:3]))
    rgbs = numpy.asarray(rgbs)
    return rgbs

def get_eigenvectors(rgbs, mean_rgb):
    pca = PCA()
    pca.fit(rgbs - mean_rgb)
    eigenvectors = pca.components_
    return eigenvectors

def get_mean_rgb(rgbs):
    return numpy.average(rgbs, axis = 0)

def get_i_projections(rgbs, mean_rgb, eigenvectors):
    i_projections = []
    for i in range(0, rgbs.shape[0]):
        i_projections.append(numpy.dot(rgbs[i] - mean_rgb, eigenvectors[0]))
    i_projections = numpy.asarray(i_projections)
    return i_projections

def get_i_projections_histogram(i_projections):
    i_hist = ArrayHelper.mean_smooth(numpy.histogram(i_projections, bins = BINS, normed = False)[0], SMOOTH_WINDOW)
    i_hist /= numpy.trapz(i_hist)
    return i_hist

'''attempts to find the normal distribution best curve fit of the histogram function.
This is used to see how closely the normal distribution fits the histogram'''
def get_normal_distribution_estimation(i_hist, i_projections):
    mean = numpy.argmax(i_hist)
    std_dev = numpy.std(i_projections, dtype = numpy.float64)
    out_arr = numpy.zeros((i_hist.shape[0]))
    base = 1.0/(sqrt(2.0 * pi * std_dev**2))
    for i in range(0, out_arr.shape[0]):
        index_val = base * exp(- (float(i - mean)**2)/(2.0 * std_dev**2))
        out_arr[i] = index_val
    height_ratio = numpy.amax(i_hist)/numpy.amax(out_arr)
    out_arr *= height_ratio
    std_dev /= numpy.trapz(out_arr)
    for i in range(0, out_arr.shape[0]):
        index_val = base * exp(- (float(i - mean)**2)/(2.0 * std_dev**2))
        out_arr[i] = index_val
    out_arr /= numpy.trapz(out_arr)
    return out_arr

'''returns only the squared histogram difference between the inputted image
and the estimated normal distriubiton fit. Use for picking a good threshold value'''
def get_avg_squared_histogram_difference_of_img(img, image):
    rgbs = get_rgbs(img, image)
    mean_rgb = get_mean_rgb(rgbs)
    eigenvectors = get_eigenvectors(rgbs, mean_rgb)
    i_projections = get_i_projections(rgbs, mean_rgb, eigenvectors)
    i_hist = get_i_projections_histogram(i_projections)
    normal_dist = get_normal_distribution_estimation(i_hist, i_projections)
    return get_avg_squared_histogram_difference(i_hist, normal_dist)

def get_avg_squared_histogram_difference(i_hist, fit_hist):
    return numpy.trapz(numpy.square(i_hist - fit_hist))/float(i_hist.shape[0])
