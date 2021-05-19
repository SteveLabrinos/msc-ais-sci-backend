"""
    File name: encode_faces.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 20/5/2021
    Date last modified: 20/5/2021
    Python Version: 3.8
"""
from imutils import paths
from image_recognition import recognize_faces


def get_screen_time(movie: str) -> dict:
    # all the frames from the videos
    frame_paths = list(paths.list_images("./dataset/movies/" + movie + "/frames"))
    # the trained encoding dataset for the classification model
    encodings = "./encodings/" + movie + "_encodings.picke"

    actor_screen_time = dict()
    # get the faces and recognize the actors based on the trained model for all the frames
    for frame in frame_paths:
        actors = recognize_faces(encodings, frame, model="hog")
        # calculate actors screen time based on the different frames recognized
        # because the program extracts one frame per second
        for actor in actors:
            actor_screen_time[actor] = actor_screen_time.get(actor, 0) + 1

    # print(actor_screen_time)
    return actor_screen_time
