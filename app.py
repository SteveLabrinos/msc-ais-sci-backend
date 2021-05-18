"""
    File name: app.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 18/5/2021
    Date last modified: 19/5/2021
    Python Version: 3.8
"""

from flask import Flask
from image_dataset import create_image_dataset
from encode_faces import face_encoding

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

# if the movie is not in the DB calculate the image encodings
face_encoding("jurassic_park")


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





