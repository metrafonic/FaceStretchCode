

import face_recognition
from sklearn import svm
from joblib import dump, load
import os


def train(train_folder, model_filename):
    encodings = []
    names = []
    for person in next(os.walk(train_folder))[1]:
        persondir = os.path.join(train_folder, person)
        pix = os.listdir(persondir)

        # Loop through each training image for the current person
        for person_img in pix:
            # Get the face encodings for the face in each image file
            imgfile = os.path.join(train_folder, person, person_img)
            face = face_recognition.load_image_file(imgfile)
            face_bounding_boxes = face_recognition.face_locations(face)

            # If training image contains exactly one face
            if len(face_bounding_boxes) == 1:
                face_enc = face_recognition.face_encodings(face)[0]
                # Add face encoding for current image with corresponding label (name) to the training data
                encodings.append(face_enc)
                names.append(person)
            else:
                continue
    # Create and train the SVC classifier
    clf = svm.SVC(gamma='scale')
    clf.fit(encodings, names)
    dump(clf, model_filename)
    return clf

def test(clf, test_folder):
    for person in next(os.walk(test_folder))[1]:
        persondir = os.path.join(test_folder, person)
        for image_name in next(os.walk(persondir))[2]:
            image_filepath = os.path.join(persondir, image_name)
            test_image = face_recognition.load_image_file(image_filepath)
            if len(face_recognition.face_locations(test_image)) != 1:
                print("%s,unknown,False" % (person))
                continue
            test_image_enc = face_recognition.face_encodings(test_image)[0]
            name = clf.predict([test_image_enc])
            print("%s,%s,%s" % (person,name[0], bool(name==person)))


if __name__ == "__main__":
    import sys
    trainfolder = sys.argv[1]
    testfolder = sys.argv[2]
    modelfile = os.path.join(trainfolder, "svm.joblib")
    if not os.path.exists(modelfile):
        clf = train(trainfolder, modelfile)
    else:
        clf = load(modelfile)
    test(clf, testfolder)







