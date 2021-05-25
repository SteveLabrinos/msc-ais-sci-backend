"""
    File name: encode_faces.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 19/5/2021
    Date last modified: 25/5/2021
    Python Version: 3.8
"""

# Using OpenCV and deep learning to encode
# the images from the dataset using a trained
# neural network and output 128-d embeddings

from imutils import paths
import face_recognition
import pickle
import cv2
import os


def face_encoding(movie: str, model="hog"):
    print("[INFO] quantifying faces...")
    image_paths = list(paths.list_images(f"./dataset/actors/{movie}"))

    known_encodings = []
    known_names = []

    # loop over the image paths
    for (i, image_path) in enumerate(image_paths):
        # extract the person name from the image path
        print(f"[INFO] processing image {i + 1}/{len(image_paths)}")
        name = image_path.split(os.path.sep)[-2]
        # load the input image and convert it from BGR (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(image_path)
        # convert to rgb in order to use it with dlib
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the coordinates of the bounding boxes
        # corresponding to each face in the input image
        # use hog or cnn models (hog is faster but less accurate)
        boxes = face_recognition.face_locations(rgb, model=model)
        # compute the facial embedding for the face
        # creating a 128-d face embedding
        encodings = face_recognition.face_encodings(rgb, boxes)
        # images with more than 1 face are invalid for a persons encodings dataset
        if len(encodings) > 1:
            print(f"[INFO] faces found: {len(encodings)}. Skipping image encoding...")
            continue
        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to the set of known names and encodings
            known_encodings.append(encoding)
            known_names.append(name)

        # save encodings and names
        print("[INFO] serializing encodings...")
        data = {"encodings": known_encodings, "names": known_names}
        f = open(f"./encodings/{movie}.pickle", "wb")
        f.write(pickle.dumps(data))
        f.close()
