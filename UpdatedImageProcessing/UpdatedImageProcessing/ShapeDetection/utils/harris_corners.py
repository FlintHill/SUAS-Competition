import cv2
import numpy
import math
from .cluster import Clusters, Cluster

CV_HARRIS_CORNER_THRESHOLD = 10e-03
MIN_CORNER_CLUSTER = 1

def init_harris_corners_and_cluster(monochrome_pil_img, polar_side_maximums, polar_side_minimums, origin):
    harris_img = cv2.cornerHarris(numpy.array(monochrome_pil_img), 3, 3, 0.04)
    harris_corners = []
    for x in range(0, harris_img.shape[0]):
        for y in range(0, harris_img.shape[1]):
            if harris_img[x,y] > CV_HARRIS_CORNER_THRESHOLD:
                harris_corners.append((x,y))
    maxes_and_mins = list(polar_side_maximums)
    for i in range(0, len(polar_side_minimums)):
        maxes_and_mins.append(polar_side_minimums[i])
    for i in range(0, len(maxes_and_mins)):
        radius = maxes_and_mins[i][1]
        angle = maxes_and_mins[i][0]
        dx = int(radius * math.cos(angle))
        dy = int(radius * math.sin(angle))
        pixel = (origin[0] + dx, origin[1] - dy)
        maxes_and_mins[i] = Cluster(pixel)
    clusters = Clusters(harris_corners, maxes_and_mins)
    clusters.fit_data_to_clusters(1, 0)
    #remove_clusters_with_corners_under_threshold
    i = 0
    while i < len(clusters):
        if len(clusters[i]) <= MIN_CORNER_CLUSTER:
            del clusters[i]
        else:
            i += 1
    return len(clusters)
