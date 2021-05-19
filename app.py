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
from video_frames import produce_video_frames
from screen_time import get_screen_time
import video_search as vs

# get the actors from the movie api
movie_actors = [
    "Alan Grant",
    "Claire Dearing",
    "Ellie Sattler",
    "Ian Malcolm",
    "John Hammond",
    "Owen Grady"
]

# create the dataset based on the movie actors
for actor in movie_actors:
    dataset_creation = create_image_dataset(actor)
# movie example
movie = "jurassic_park"
# if the movie is not in the DB calculate the image encodings
# face_encoding("jurassic_park")

# search for videos on YouTube based on the user input
query_string = "jurassic park"
response = vs.youtube_search(query_string)
results = vs.deserialize_response(response)
for k, v in results.items():
    print(f"{k}: {v}")

# download the videos from the movie


# produce the frames for the video
produce_video_frames("jurassic_park", "Jurassic_Park_Scene.mp4")

# calculate actor screen time
actor_screen_time = get_screen_time(movie)
for k, v in actor_screen_time.items():
    print(f"Actor: {k}\t\tScreen Time: {v} sec")


# for k, v in actor_screen_time.items():
#     print(f"Actor: {k}\t\tScreen Time: {v} sec")
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
