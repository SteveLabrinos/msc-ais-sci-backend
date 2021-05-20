"""
    File name: app.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 18/5/2021
    Date last modified: 20/5/2021
    Python Version: 3.8
"""

from flask import Flask
from imutils import paths
from image_dataset import create_image_dataset
from encode_faces import face_encoding
from image_recognition import recognize_faces
import video_frames as vf
from screen_time import get_screen_time
import video_search as vs
from video_download import download_youtube_list

# Downloading a sample of the list to reduce time results
MAX_VIDEO_SEARCH = 3

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
response = vs.youtube_search(query_string, MAX_VIDEO_SEARCH)
youtube_videos = vs.deserialize_response(response)

# download the videos from the movie
# download_youtube_list(movie, youtube_videos['video_id'])

# produce the frames for the video
# vf.process_video_list("jurassic_park")

# calculate actor screen time
youtube_videos['screen_times'] = get_screen_time(
    movie, len(youtube_videos['video_id']))

# print the YouTube video list
for k, v in youtube_videos.items():
    print(f"{k}: {v}")


# app = Flask(__name__)

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
