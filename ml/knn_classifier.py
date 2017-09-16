# http://www.pyimagesearch.com/2016/08/08/k-nn-classifier-for-image-classification/

from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split
from imutils import paths
from preprocess import image_to_feature_vector, extract_color_histogram

import numpy as np
import argparse
import imutils
import cv2
import os
import pickle
import pandas
import matplotlib.pyplot as plt

# grab the list of images that we'll be describing
IMAGES_PATH = "../images"
print("[INFO] describing images...")
imagePaths = list(paths.list_images(IMAGES_PATH))
 
# initialize the raw pixel intensities matrix, the features matrix,
# and labels list
rawImages = []
features = []
labels = []


# loop over the input images
for (i, imagePath) in enumerate(imagePaths):
    # load the image and extract the class label (assuming that our
    # path as the format: /path/to/dataset/{class}.{image_num}.jpg
    image = cv2.imread(imagePath)
    if image is not None:
        label = imagePath.split(os.path.sep)[-1].split("_")[0]
    
        # extract raw pixel intensity "features", followed by a color
        # histogram to characterize the color distribution of the pixels
        # in the image
        pixels = image_to_feature_vector(image)
        hist = extract_color_histogram(image)
    
        # update the raw images, features, and labels matricies,
        # respectively
        rawImages.append(pixels)
        features.append(hist)
        labels.append(label)
    
        # show an update every 1,000 images
        if i > 0 and i % 1000 == 0:
            print("[INFO] processed {}/{}".format(i, len(imagePaths)))


# show some information on the memory consumed by the raw images
# matrix and features matrix
rawImages = np.array(rawImages)
features = np.array(features)
labels = np.array(labels)
print("[INFO] pixels matrix: {:.2f}MB".format(
    rawImages.nbytes / (1024 * 1000.0)))
print("[INFO] features matrix: {:.2f}MB".format(
    features.nbytes / (1024 * 1000.0)))


# partition the data into training and testing splits, using 75%
# of the data for training and the remaining 25% for testing
(trainRI, testRI, trainRL, testRL) = train_test_split(
    rawImages, labels, test_size=0.25, random_state=42)
(trainFeat, testFeat, trainLabels, testLabels) = train_test_split(
    features, labels, test_size=0.25, random_state=42)

# train and evaluate a k-NN classifer on the raw pixel intensities
print("[INFO] evaluating raw pixel accuracy...")
model = KNeighborsClassifier(n_neighbors=1,
    n_jobs=1)
model.fit(trainRI, trainRL)
acc = model.score(testRI, testRL)
print("[INFO] raw pixel accuracy: {:.2f}%".format(acc * 100))


# train and evaluate a k-NN classifer on the histogram
# representations
print("[INFO] evaluating histogram accuracy...")
model = KNeighborsClassifier(n_neighbors=1,
    n_jobs=1)
model.fit(trainFeat, trainLabels)
acc = model.score(testFeat, testLabels)
print("[INFO] histogram accuracy: {:.2f}%".format(acc * 100))

# save trained model to a pickle file
filename = "knn_model.sav"
pickle.dump(model, open(filename, 'wb'))
