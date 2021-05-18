"""
    File name: app.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 18/5/2021
    Date last modified: 19/5/2021
    Python Version: 3.8
"""

from flask import Flask
from imutils import paths
from image_dataset import create_image_dataset
from encode_faces import face_encoding
from image_recognition import recognize_faces

movie_actors = [
    "Alan Grant",
    "Claire Dearing",
    "Ellie Sattler",
    "Ian Malcolm",
    "John Hammond",
    "Owen Grady"
]

for actor in movie_actors:
    dataset_creation = create_image_dataset(actor)

# movie example
movie = "jurassic_park"
# if the movie is not in the DB calculate the image encodings

# face_encoding("jurassic_park")

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
for k, v in actor_screen_time.items():
    print(f"Actor: {k}\t\tScreen Time: {v} sec")
# app = Flask(__name__)
#
#
# @app.route('/')
# def hello_world():
#     create_image_dataset("Keanu Reeves")
#     return 'Hello World!'
#
#
# if __name__ == '__main__':
#     create_image_dataset("Keanu Reeves")
#     app.run()
