# import the necessary packages
from imutils import paths
import face_recognition
import argparse
from joblib import dump, load
import cv2
import os
import glob


def encode(dataset, encodings_file, method):
    # grab the paths to the input images in our dataset
    print("[INFO] quantifying faces...")
    print(dataset)
    imagePaths = glob.glob(os.path.join(dataset, "**/*.pgm"))
    # initialize the list of known encodings and known names
    knownEncodings = []
    knownNames = []


    # loop over the image paths
    for (i, imagePath) in enumerate(imagePaths):
        # extract the person name from the image path
        print("[INFO] processing image {}/{}".format(i + 1,
                                                     len(imagePaths)))
        name = os.path.basename(os.path.dirname(imagePath))
        # load the input image and convert it from BGR (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb,
                                                model=method)
        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)
        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to our set of known names and
            # encodings
            knownEncodings.append(encoding)
            knownNames.append(name)
    # dump the facial encodings + names to disk
    print("[INFO] serializing encodings...")
    print(f"{len(knownEncodings)}, {len(knownNames)}")
    data = {"encodings": knownEncodings, "names": knownNames}
    if not os.path.exists(os.path.dirname(encodings_file)):
        os.makedirs(os.path.dirname(encodings_file))
    dump(data, encodings_file)

def recognize(encodings_file, image_dir, method, csv_file):
    data = load(encodings_file)
    # load the input image and convert it from BGR to RGB
    recognition_info_file = f"{os.path.splitext(csv_file)[0]}-faces.txt"
    with open(recognition_info_file, 'a+', encoding='utf-8') as f:
        f.write(f"{len(data['encodings'])}")
    print("[INFO] predicting faces...")
    for person in next(os.walk(image_dir))[1]:
        persondir = os.path.join(image_dir, person)
        for image_name in next(os.walk(persondir))[2]:
            image_filepath = os.path.join(persondir, image_name)
            image = cv2.imread(image_filepath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # detect the (x, y)-coordinates of the bounding boxes corresponding
            # to each face in the input image, then compute the facial embeddings
            # for each face
            boxes = face_recognition.face_locations(rgb,
                                                    model=method)
            encodings = face_recognition.face_encodings(rgb, boxes)
            # initialize the list of names for each face detected
            # loop over the facial embeddings
            encoding = None
            database_encoding = None
            name = "unknown"
            if encodings:
                encoding = encodings[0]
                matches = face_recognition.api.face_distance(data["encodings"],
                                                         encoding)
                matches = list(matches)
                index = matches.index(min(matches))
                name = data["names"][index]
                distance = matches[index]
            # loop over the recognized faces
            distance = 1
            correct_guess = bool(person == name)
            with open(csv_file, 'a+', encoding='utf-8') as f:
                f.write("%i,%f,%s,%s,%s" % (correct_guess, 1 - distance, person, name, correct_guess) + "\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True,
                    help="path to input directory of faces + images")
    ap.add_argument("-e", "--encodings", required=True,
                    help="path to serialized db of facial encodings")
    ap.add_argument("-d", "--detection-method", type=str, default="cnn",
                    help="face detection model to use: either `hog` or `cnn`")
    ap.add_argument("-i", "--image", required=True,
                    help="path to input image dataset")
    ap.add_argument("-o", "--out", required=True,
                    help="path to csv file")
    args = vars(ap.parse_args())
    if not os.path.exists(args["encodings"]):
        encode(args["dataset"], args["encodings"], args["detection_method"])
    recognize(args["encodings"], args["image"], args["detection_method"], args["out"])

if __name__ == "__main__":
    main()