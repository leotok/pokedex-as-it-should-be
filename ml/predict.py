from sklearn.neighbors import KNeighborsClassifier
from preprocess import image_to_feature_vector, extract_color_histogram

import argparse
import os
import cv2
import imutils
import pickle
import numpy as np

FULL_UPLOAD_PATH = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "api")
MODEL_PATH = os.path.dirname(os.path.abspath(__file__))

def predict_pokemon(imagePath):
    fullpath = FULL_UPLOAD_PATH + imagePath
    image = cv2.imread(fullpath)
    if image is not None:
        features = np.array([extract_color_histogram(image)])
        loaded_model = pickle.load(open(MODEL_PATH + "/pokemon_model.sav", 'rb'))

        return loaded_model.predict(features)[0]
    else:
        raise "Failed"