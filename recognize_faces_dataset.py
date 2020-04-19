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
    data = load(args["encodings"])
    # load the input image and convert it from BGR to RGB
    for person in next(os.walk(args["image"]))[1]:
        persondir = os.path.join(args["image"], person)
        for image_name in next(os.walk(persondir))[2]:
            image_filepath = os.path.join(persondir, image_name)
            image = cv2.imread(image_filepath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # detect the (x, y)-coordinates of the bounding boxes corresponding
            # to each face in the input image, then compute the facial embeddings
            # for each face
            boxes = face_recognition.face_locations(rgb,
                                                    model=args["detection_method"])
            encodings = face_recognition.face_encodings(rgb, boxes)
            # initialize the list of names for each face detected
            names = []
            # loop over the facial embeddings
            sample_encodings = {}
            database_encodings = {}
            for encoding in encodings:
                # attempt to match each face in the input image to our known
                # encodings
                matches = face_recognition.compare_faces(data["encodings"],
                                                         encoding)
                name = "Unknown"
                name_id = None
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
                    if names_encoding:
                        name_id = names_encoding[name]

                # update the list of names
                names.append(name)

                sample_encodings[name] = encoding
                database_encodings[name] = data["encodings"][name_id]
            # loop over the recognized faces
            name = "unkonown"
            distance = 1
            if names:
                name = names[0]
                distance = face_recognition.api.face_distance([database_encodings[name]], sample_encodings[name])[0]
            correct_guess = bool(person == name)
            print("%i,%f,%s,%s,%s" % (correct_guess, 1-distance, person,name, correct_guess))

if __name__ == "__main__":
    main()