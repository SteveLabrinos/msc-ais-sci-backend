"""
    File name: encode_faces.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 19/5/2021
    Date last modified: 20/5/2021
    Python Version: 3.8
"""
# recognize faces for given images based on the face embeddings
# using openCV and deep learning
import face_recognition
import pickle
import cv2


# functions parameters: encodings.pickle path, the frame image, the model
# HOG method is preferred for single CPU
def recognize_faces(encodings_path, image_path, model="hog"):
    # load the known faces and embeddings from the pickle file
    data = pickle.loads(open(encodings_path, "rb").read())
    # load the input image and convert it from BGR to RGB
    image = cv2.imread(image_path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # detect the coordinates of the bounding boxes corresponding
    # to each face in the input image, then compute the facial embeddings for each face
    boxes = face_recognition.face_locations(rgb, model=model)
    encodings = face_recognition.face_encodings(rgb, boxes)
    # initialize the list of names for each face detected
    names = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to the known
        # movie actors encodings using Euclidean distance between encodings
        # using a k-NN classification model to classify as True or False
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        # default name if no known actor is found
        name = "Unknown"
        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a dictionary
            # to count the total number of times each face was matched
            matched_indexes = [i for (i, b) in enumerate(matches) if b]
            # {key: name, value: True counts}
            counts = dict()
            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matched_indexes:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            # determine the recognized face with the largest number of
            # votes (in the event of an  tie first entry is selected)
            name = max(counts, key=counts.get)

        # update the list of names
        if name != "Unknown":
            names.append(name)
    # print(f"[INFO] Found {len(names)} actors for the given image")
    # return the recognized faces found for the image
    return names
