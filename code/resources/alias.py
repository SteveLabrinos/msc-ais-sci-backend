"""
    File name: app.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 24/5/2021
    Date last modified: 24/5/2021
    Python Version: 3.8
"""

from flask_restful import Resource
from movie_search import get_movie
from code.models.alias import MovieAliasModel
from code.models.movie import MovieModel


class MovieAlias(Resource):
    def get(self, alias):
        # search if the has been previous movie search with the same alias
        alias_result = MovieAliasModel.find_by_alias(alias)
        # if the was a previous search skip the IMDB API call
        if alias_result:
            return MovieModel.find_by_id(alias_result.movie_id).json()
        # search for the movie in IMDB and store it to the movie model
        movie_api = get_movie(alias)
        # if the search dont yield any results
        if movie_api is None:
            return {'message': f'No movie found for alias {alias}'}

        movie = MovieModel(**movie_api)
        movie_alias = MovieAliasModel(alias, movie.id)

        # save to models to the DB
        if MovieModel.find_by_id(movie.id) is None:
            movie.save_to_db()
        movie_alias.save_to_db()
        # return the movie from the API call
        return movie.json()



        # return {'message': 'No alias found! Search to IMDB'}
