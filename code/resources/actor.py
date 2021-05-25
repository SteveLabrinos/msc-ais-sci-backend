"""
    File name: app.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 24/5/2021
    Date last modified: 24/5/2021
    Python Version: 3.8
"""

from flask_restful import Resource
from code.deep_learning.image_dataset import create_image_dataset
from code.deep_learning.encode_faces import face_encoding
from code.deep_learning.screen_time import get_screen_time
from code.models.actor import ActorModel
from code.models.movie import MovieModel


class Actor(Resource):
    def get(self, actor_id):
        actor = ActorModel.find_by_id(actor_id)
        if actor:
            return actor.json()
        return {'message': f'Actor with id {actor_id} not found'}, 404


class ActorDataset(Resource):
    def get(self, movie_id, size):
        movie = MovieModel.find_by_id(movie_id)
        no_dataset_actors = list(filter(lambda a: a.dataset is None, movie.actors))

        # if all actors have a dataset dont re-download
        if len(no_dataset_actors) == 0:
            return {'message': 'dataset is complete'}

        # download images for each actor with empty dataset
        for actor in no_dataset_actors:
            create_image_dataset(actor.id, movie_id, size)
            # save the the size of the dataset for the actor
            ActorModel.update_dataset_by_id(actor_id=actor.id, size=size)

        return {'message': f'downloaded {size} images for the {len(no_dataset_actors)} actors'}


class ActorEncoding(Resource):
    def get(self, movie_id, learning_model):
        # check if the movie already has encoded its actors
        movie = MovieModel.find_by_id(movie_id)
        if movie.encodings:
            return {'message': 'Actor encodings is complete'}
        # create the pickle file with the encodings
        # for all the actors of the given movie
        try:
            face_encoding(movie_id, learning_model)
        except Exception as e:
            return {'message': f'Error occurred when trying to encode actors dataset - {e}'}, 500

        # update that the movie has encodings
        movie.encodings = 'completed'
        movie.save_to_db()
        return {'message': f'Encoding of all actors completed'}


class ActorScreenTime(Resource):
    def get(self, movie_id, learning_model):
        movie = MovieModel.find_by_id(movie_id)
        count = movie.videos.count()
        # for i in movie.videos:
        #     cnt += 1
        # check if the screen times are calculated
        videos_screen_times = get_screen_time(
            movie_id, count, learning_model
        )
        # test
        for v in videos_screen_times:
            print(v)

        return {'message': 'video screen times calculated'}


