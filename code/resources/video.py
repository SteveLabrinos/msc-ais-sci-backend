"""
    File name: app.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 24/5/2021
    Date last modified: 25/5/2021
    Python Version: 3.8
"""

from flask_restful import Resource
from code.models.video import VideoModel
from code.models.movie import MovieModel
from code.deep_learning.video_search import youtube_search, deserialize_response
from globals import MAX_VIDEO_SEARCH


class Video(Resource):
    def get(self, movie_id):
        # check if the videos exist in the database
        videos = VideoModel.find_by_movie(movie_id)
        if videos:
            return {'videos': [v.json() for v in videos]}

        # download the videos with the YouTube API
        movie = MovieModel.find_by_id(movie_id)
        query_string = f'{movie.title} & {movie.year}'
        response = youtube_search(query=query_string, max_results=MAX_VIDEO_SEARCH)
        youtube_videos = deserialize_response(response)

        for video in youtube_videos:
            v = VideoModel(**video)
            v.movie_id = movie_id
            v.save_to_db()

        videos = VideoModel.find_by_movie(movie_id)
        return {'message': [v.json() for v in videos]}