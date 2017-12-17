from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
from imutils import paths
from preprocess import image_to_feature_vector, make_standard

from keras.models import Sequential
from keras.layers import Activation, Dense
from keras.optimizers import SGD
from keras.utils import np_utils

import numpy as np
import imutils
import cv2
import os
import pickle
import pandas


IMAGES_PATH = "../images"
print("[INFO] describing images...")
imagePaths = list(paths.list_images(IMAGES_PATH))
 
# initialize the raw pixel intensities matrix, the features matrix,
# and labels list
features = []
labels = []
num_classese = 6

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


le = LabelEncoder()
labels = le.fit_transform(labels)
labels = np_utils.to_categorical(labels, num_classese)

features = np.array(features) / 255.0

# partition the data into training and testing splits, using 75%
# of the data for training and the remaining 25% for testing
trainData, testData, trainLabels, testLabels = train_test_split(features, labels, test_size=0.25, random_state=42)

model = Sequential()
model.add(Dense(768, input_dim=3072, init="uniform", activation="relu"))
model.add(Dense(384, init="uniform", activation="relu"))
model.add(Dense(num_classese))
model.add(Activation("softmax"))

print ("[INFO] compiling model...")
sgd = SGD(lr=0.008)
model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])
model.fit(trainData, trainLabels, nb_epoch=50, batch_size=128)

print ("[INFO] evaluating on testing set...")
loss, accuracy = model.evaluate(testData, testLabels, batch_size=128, verbose=1)
print ("[INFO] loss = {:.4f}, accuracy = {:.4f}%".format(loss, accuracy * 100))

# save trained model to a pickle file
filename = "keras_simple_nn.sav"
model.save(filename)
