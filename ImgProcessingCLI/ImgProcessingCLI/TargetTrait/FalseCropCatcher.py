import ImgProcessingCLI.Array.ArrayHelper as ArrayHelper
import numpy
from sklearn.decomposition import PCA
import scipy
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

BINS = 100#500
SMOOTH_WINDOW = 25#20#50
DIR_SMOOTH_WINDOW = 10

'''the below are the most suited to optimization -- especially probability density threshold'''

'''the minimum number of maxima for the target to be classified as not a false positive'''
NUM_MAXES_THRESHOLD = 1
'''must be a value between 0 and 1'''
PROBABILITY_DENSITY_THRESHOLD = .12#0
#MIN_DISTRIBUTION_PEAK = 0
MIN_IHIST_DIR_VAL = .00002


def get_if_is_false_positive(img, image):

    rgbs = []
    for x in range(0, img.size[0]):
        for y in range(0, img.size[1]):
            rgbs.append(image[x,y][0:3])
    rgbs = numpy.asarray(rgbs)
    pca = PCA()
    pca.fit(rgbs)
    eigenvectors = pca.components_

    mean = numpy.average(rgbs, axis = 0)

    i_projections = []
    for i in range(0, rgbs.shape[0]):
        i_projections.append(numpy.dot(numpy.asarray(rgbs[i]) - mean, eigenvectors[0]))

    i_projections = numpy.asarray(i_projections)

    i_hist = ArrayHelper.mean_smooth(numpy.histogram(i_projections, bins = BINS, normed = False)[0], SMOOTH_WINDOW)

    i_hist = i_hist - numpy.amin(i_hist)
    i_hist /= numpy.amax(i_hist)

    i_hist_density = scipy.integrate.cumtrapz(i_hist)#numpy.polyint(i_hist)
    log_fit = LogisticRegression()
    log_fit.fit(numpy.array([0 for i in range(0, i_hist_density.shape[0])]), i_hist_density)



    i_hist_dir = ArrayHelper.mean_smooth(numpy.gradient(i_hist), DIR_SMOOTH_WINDOW)
    maxes = ArrayHelper.get_maxes(i_hist_dir)
    mins = ArrayHelper.get_mins(i_hist_dir)
    mins = list(mins)
    mins.insert(0, 0)
    mins.append(i_hist.shape[0])
    mins = numpy.asarray(mins)

    plt.clf()
    plt.plot(i_hist)
    plt.axvline(0)
    plt.axhline(0)
    plt.show()

    plt.clf()
    plt.plot(i_hist_density)
    plt.axvline(0)
    plt.axhline(0)
    plt.show()


    num_thresholded_maxes = 0

    '''would probably be best if this were a decision tree'''
    for i in range(0, maxes.shape[0]):

        '''weeds out the majority of the false positives (roughly 80%) with very little loss in false negatives (1%)'''
        if i_hist_dir[maxes[i]] > MIN_IHIST_DIR_VAL:
            num_thresholded_maxes += 1
        else:
            min_indexes = None
            indexes_found = False
            j=0
            while j < mins.shape[0]-1 and indexes_found == False:
                if maxes[i] >= mins[j] and maxes[i] <=mins[j+1]:
                    min_indexes = (j, j+1)
                    indexes_found = True
                j += 1

            '''weeds out even more false positives with no noticeable affect on false negatives'''
            if min_indexes != None and i_hist_density[min_indexes[1]] - i_hist_density[min_indexes[0]] > PROBABILITY_DENSITY_THRESHOLD:
                num_thresholded_maxes += 1


    return (num_thresholded_maxes<=NUM_MAXES_THRESHOLD)
