from sklearn.neural_network import MLPClassifier
from sklearn.cross_validation import train_test_split
from imutils import paths
from preprocess import image_to_feature_vector, make_standard

import numpy as np
import imutils
import cv2
import os
import pickle
import pandas
import matplotlib.pyplot as plt


IMAGES_PATH = "../images"
print("[INFO] describing images...")
imagePaths = list(paths.list_images(IMAGES_PATH))
 
# initialize the raw pixel intensities matrix, the features matrix,
# and labels list
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
        
        pixels = image_to_feature_vector(image)
    
        features.append(pixels)
        labels.append(label)
    
        # show an update every 1,000 images
        if i > 0 and i % 20 == 0:
            print("[INFO] processed {}/{}".format(i, len(imagePaths)))


# show some information on the memory consumed by the raw images
# matrix and features matrix
features = np.array(features)
labels = np.array(labels)
print("[INFO] features matrix: {:.2f}MB".format(
    features.nbytes / (1024 * 1000.0)))


# partition the data into training and testing splits, using 75%
# of the data for training and the remaining 25% for testing

(trainFeat, testFeat, trainLabels, testLabels) = train_test_split(
    features, labels, test_size=0.25, random_state=42)

trainFeat, testFeat = make_standard(trainFeat, testFeat)




# train and evaluate a k-NN classifer on the raw pixel intensities
print("[INFO] evaluating MLP accuracy...")
model = MLPClassifier(solver='lbfgs', 
                      hidden_layer_sizes=(200, 80, 50), activation="relu", random_state=1)
model.fit(trainFeat, trainLabels)
acc = model.score(testFeat, testLabels)
print("[INFO] MLP accuracy: {:.2f}%".format(acc * 100))


# save trained model to a pickle file
filename = "mlp_model.sav"
pickle.dump(model, open(filename, 'wb'))
