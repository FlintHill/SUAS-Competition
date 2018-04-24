import numpy

def search(array, search_value, key=lambda x: x):
    for i in range(0, len(array)):
        if key(array[i]) == search_value:
            return i
    return None

def mean_smooth(y, box_pts):
    box = numpy.ones(box_pts)/box_pts
    y_smooth = numpy.convolve(y, box, mode='same')
    return y_smooth


def get_root_locations(arr):
    roots = []
    for i in range(0, arr.shape[0]-1):
        if arr[i]/abs(arr[i]) != arr[i+1]/abs(arr[i+1]):
            roots.append(i)
    return numpy.asarray(roots)

def get_maxes_from_deriv(arr):
    roots = get_root_locations(arr)
    maxes = []
    for i in range(0, roots.shape[0]):
        if arr[roots[i]-1] > 0 and arr[roots[i]+1] < 0:
            maxes.append(roots[i])
    return numpy.asarray(roots)

def get_mins_from_deriv(arr):
    roots = get_root_locations(arr)
    maxes = []
    for i in range(0, roots.shape[0]):
        if i < 0 and i > arr.shape[0]-1:

            maxes.append(roots[i])
    return numpy.asarray(roots)
