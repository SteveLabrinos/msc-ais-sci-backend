"""
    File name: video.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 24/5/2021
    Date last modified: 27/5/2021
    Python Version: 3.8
"""

from flask_restful import Resource
from imutils import paths
from code.models.video import VideoModel
from code.models.movie import MovieModel
from code.deep_learning.video_search import youtube_search, deserialize_response
from code.deep_learning.video_download import download_youtube_list
from code.deep_learning.video_frames import produce_video_frames


class Video(Resource):
    def get(self, movie_id, total_videos):
        # check if the videos exist in the database
        videos = VideoModel.find_by_movie(movie_id)
        if videos:
            return {'videos': [v.json() for v in videos]}

        # download the videos with the YouTube API
        movie = MovieModel.find_by_id(movie_id)
        query_string = f'{movie.title} & {movie.year}'
        response = youtube_search(query=query_string, max_results=total_videos)
        youtube_videos = deserialize_response(response)

        for video in youtube_videos:
            v = VideoModel(**video)
            v.movie_id = movie_id
            v.save_to_db()

        videos = VideoModel.find_by_movie(movie_id)
        return {'videos': [v.json() for v in videos]}


class VideoDownload(Resource):
    def get(self, movie_id):
        # check if the videos have already been downloaded
        path = f"./dataset/movies/{movie_id}/videos"
        videos_path = list(paths.list_files(path))
        if len(videos_path) > 0:
            return {'message': 'Videos have already been downloaded'}
        # get the videos for the given movie
        try:
            movie = MovieModel.find_by_id(movie_id)
        except Exception as e:
            return {'message': f'Error occurred while downloading videos from YouTube: {e}'}, 500

        video_id_list = [v.id for v in movie.videos]
        download_youtube_list(movie=movie_id, video_ids=video_id_list)
        return {'message': f'Video download completed for {len(video_id_list)} videos'}


class VideoFrames(Resource):
    def get(self, movie_id):
        # check if the frames have already been produced
        path = f"./dataset/movies/{movie_id}/frames"
        frames_path = list(paths.list_files(path))
        if len(frames_path) > 0:
            return {'message': 'Frames have already been produced'}

        # get the frames for the movies downloaded videos
        movie = MovieModel.find_by_id(movie_id)
        for video in movie.videos:
            try:
                produce_video_frames(movie_id, video.id)
            except Exception as e:
                return {'message': f'Error occurred while producing video frames - {e}'}, 500

        return {'message': 'Video frames produced'}

