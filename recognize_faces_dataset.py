# import the necessary packages
import face_recognition
import argparse
from joblib import dump, load
import cv2
import os


def main():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--encodings", required=True,
        help="path to serialized db of facial encodings")
    ap.add_argument("-i", "--image", required=True,
        help="path to input image dataset")
    ap.add_argument("-d", "--detection-method", type=str, default="cnn",
        help="face detection model to use: either `hog` or `cnn`")
    args = vars(ap.parse_args())
    # load the known faces and embeddings


if __name__ == "__main__":
    main()