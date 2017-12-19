from sklearn.neighbors import KNeighborsClassifier
from preprocess import image_to_feature_vector, extract_color_histogram
from sklearn.preprocessing import StandardScaler

import argparse
import os
import cv2
import imutils
import pickle
import numpy as np

FULL_UPLOAD_PATH = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "api")
MODEL_PATH = os.path.dirname(os.path.abspath(__file__))

def predict_knn(image_file):
    image = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.CV_LOAD_IMAGE_UNCHANGED)
    if image is not None:
        features = np.array([extract_color_histogram(image)])
        loaded_model = pickle.load(open(MODEL_PATH + "/knn_model.sav", 'rb'))

        return loaded_model.predict(features)[0]
    else:
        raise "Failed"


def predict_mlp(image_file):
    image = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.CV_LOAD_IMAGE_UNCHANGED)
    if image is not None:
        features = np.array([image_to_feature_vector(image)])
        loaded_model = pickle.load(open(MODEL_PATH + "/mlp_model.sav", 'rb'))
        scaler = pickle.load(open(MODEL_PATH + "/scaler_model.sav", "rb"))
        features = scaler.transform(features)

        return loaded_model.predict(features)[0]
    else:
        raise "Failed"