"""
    File name: app.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 24/5/2021
    Date last modified: 24/5/2021
    Python Version: 3.8
"""

from flask_restful import Resource
from code.models.movie import MovieModel


class Movie(Resource):
    def get(self, movie_id):
        movie = MovieModel.find_by_id(movie_id)
        if movie:
            return movie.json()
        return {'message': f'Movie with id {movie_id} not found'}, 404


class MovieList(Resource):
    def get(self):
        return {'movies': [m.json() for m in MovieModel.query.all()]}
