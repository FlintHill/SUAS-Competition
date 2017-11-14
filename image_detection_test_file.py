from PIL import Image
import PIL.ImageOps
import os
from SyntheticDataset2 import *
import cv2
import numpy as np
from matplotlib import pyplot as plt

from sklearn.cluster import MiniBatchKMeans
import argparse

"""
image = Image.open("/Users/zyin/Desktop/Synthetic Dataset/Answers/target_maps/6.jpg")

denoised_image = GaussianNoiseGenerator.generate_gaussian_noise_by_level(image, 2, image.width)
inverted_image = PIL.ImageOps.invert(denoised_image)
posterized_image = PIL.ImageOps.posterize(inverted_image, 2)
posterized_image.save("/Users/zyin/Desktop/3.jpg")

#gray_image = PIL.ImageOps.grayscale(solarized_image)
"""
from sklearn.cluster import MiniBatchKMeans
import numpy as np
import argparse
import cv2
"""
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
ap.add_argument("-c", "--clusters", required = True, type = int,
	help = "# of clusters")
args = vars(ap.parse_args())
"""

#im = cv2.imread("/Users/zyin/Desktop/2.jpg", cv2.IMREAD_COLOR)

image = cv2.imread("/Users/zyin/Desktop/Synthetic Dataset/Answers/target_maps/6.jpg", cv2.IMREAD_COLOR)
(h, w) = image.shape[:2]

image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

image = image.reshape((image.shape[0] * image.shape[1], 3))

clt = MiniBatchKMeans(8)
labels = clt.fit_predict(image)
quant = clt.cluster_centers_.astype("uint8")[labels]

quant = quant.reshape((h, w, 3))
image = image.reshape((h, w, 3))

quant = cv2.cvtColor(quant, cv2.COLOR_LAB2BGR)
image = cv2.cvtColor(image, cv2.COLOR_LAB2BGR)

cv2.imshow("image", np.hstack([image, quant]))
cv2.waitKey(0)
