# import the necessary packages
from imutils import paths
import face_recognition
import argparse
from joblib import dump, load
import cv2
import os



def encode(dataset, encodings, method):
    # grab the paths to the input images in our dataset
    print("[INFO] quantifying faces...")
    imagePaths = list(paths.list_images(dataset))
    # initialize the list of known encodings and known names
    knownEncodings = []
    knownNames = []


    # loop over the image paths
    for (i, imagePath) in enumerate(imagePaths):
        # extract the person name from the image path
        print("[INFO] processing image {}/{}".format(i + 1,
                                                     len(imagePaths)))
        name = imagePath.split(os.path.sep)[-2]
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
    data = {"encodings": knownEncodings, "names": knownNames}
    if not os.path.exists(os.path.dirname(encodings)):
        os.makedirs(os.path.dirname(encodings))
    dump(data, encodings)

def recognize(encodings_file, image_dir, method):
    data = load(encodings_file)
    # load the input image and convert it from BGR to RGB
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
            names = []
            # loop over the facial embeddings
            encoding = None
            database_encoding = None
            if encodings:
                encoding = encodings[0]
                matches = face_recognition.compare_faces(data["encodings"],
                                                         encoding, tolerance=1)
                # check to see if we have found a match
                if True in matches:
                    # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}
                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    names_encoding = {}
                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1
                        names_encoding[name] = i
                    # determine the recognized face with the largest number of
                    # votes (note: in the event of an unlikely tie Python will
                    # select first entry in the dictionary)
                    name = max(counts, key=counts.get)
                    names.append(name)
                if names:
                    name_id = names_encoding[names[0]]
                    database_encoding = data["encodings"][name_id]
            # loop over the recognized faces
            name = "unknown"
            distance = 1
            if names:
                name = names[0]
                distance = face_recognition.api.face_distance([database_encoding], encoding)[0]
            correct_guess = bool(person == name)
            print("%i,%f,%s,%s,%s" % (correct_guess, 1 - distance, person, name, correct_guess))

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
    args = vars(ap.parse_args())
    if not os.path.exists(args["encodings"]):
        encode(args["dataset"], args["encodings"], args["detection_method"])
    recognize(args["encodings"], args["image"], args["detection_method"])

if __name__ == "__main__":
    main()