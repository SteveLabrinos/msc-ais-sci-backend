"""
    File name: alias.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 24/5/2021
    Date last modified: 27/5/2021
    Python Version: 3.8
"""

from flask_restful import Resource
from code.deep_learning.movie_search import get_movie, get_cast
from code.models.alias import MovieAliasModel
from code.models.movie import MovieModel
from code.models.actor import ActorModel


class MovieAlias(Resource):
    def get(self, alias):
        alias = alias.lower().strip()
        # search if the has been previous movie search with the same alias
        alias_result = MovieAliasModel.find_by_alias(alias)
        # if the was a previous search skip the IMDB API call
        if alias_result:
            return MovieModel.find_by_id(alias_result.movie_id).json()
        # search for the movie in IMDB and store it to the movie model
        movie_api = get_movie(alias)
        # if the search dont yield any results
        if movie_api is None:
            return {'message': f'No movie found for alias {alias}'}, 404

        movie = MovieModel(**movie_api)
        movie_alias = MovieAliasModel(alias, movie.id)

        # search if the movie exists in the database
        stored_movie = MovieModel.find_by_id(movie.id)
        if stored_movie:
            movie_alias.save_to_db()
            return stored_movie.json()

        # get the actors for the given movie
        top_cast = get_cast(movie.id)
        for cast in top_cast:
            # check if the actor already exists
            actor = ActorModel.find_by_id(cast['id'])
            if actor:
                # preparing the stored actor for new update
                actor.role_name = cast['role_name']
                actor.dataset = None
            else:
                actor = ActorModel(**cast)
            movie.actors.append(actor)

        # save results of movie, actors and alias to the DB
        movie.save_to_db()
        movie_alias.save_to_db()
        # return the movie from the API call
        return movie.json()
