from sklearn.neighbors import KNeighborsClassifier
from preprocess import image_to_feature_vector, extract_color_histogram

import argparse
import os
import cv2
import imutils
import pickle
import numpy as np


def predict_pokemon(imagePath):
    image = cv2.imread(imagePath)
    if image is not None:
        features = np.array([extract_color_histogram(image)])
        loaded_model = pickle.load(open("pokemon_model.sav", 'rb'))

        return loaded_model.predict(features)[0]
    else:
        return "Faile to load image"