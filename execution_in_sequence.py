"""
    File name: execution_in_sequence.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 18/5/2021
    Date last modified: 21/5/2021
    Python Version: 3.8
"""

from code.deep_learning.image_dataset import create_image_dataset
from code.deep_learning.encode_faces import face_encoding
from code.deep_learning.screen_time import get_screen_time
from code.deep_learning import video_search as vs, video_frames as vf
from code.deep_learning.video_download import download_youtube_list
from code.deep_learning.movie_search import get_movie

# Downloading a sample of the list to reduce time results
MAX_VIDEO_SEARCH = 3

query = "inception"
model = "hog"
# 1. depending on the query from the user get the relevant movie and cast
# OK
movie = get_movie(query)

# actors name and movie role for the image dataset
# OK
movie_actors = [(lambda c: f"{c['actor_name']} - {c['role_name']}")(c) for c in movie["cast"]]

movie_name = movie["movie_title"].lower().replace(" ", "_")
# 2. create the dataset based on the movie actors
# OK
for actor in movie_actors:
    dataset_creation = create_image_dataset(actor, movie_name)

# 3. if the movie is not in the DB calculate the image encodings
# OK
face_encoding(movie_name, model="hog")

# 4. search for videos on YouTube based on the user input
# OK
you_tube_search = f"{movie['movie_title']} & {movie['year']}"
response = vs.youtube_search(you_tube_search, MAX_VIDEO_SEARCH)
youtube_videos = vs.deserialize_response(response)

# 5. download the videos from the movie
# OK
download_youtube_list(movie_name, youtube_videos['video_id'])

# 6. produce the frames for the video
# OK
vf.process_video_list(movie_name)

# 7. calculate actor screen time
youtube_videos['screen_times'] = get_screen_time(
    movie_name, len(youtube_videos['video_id']), model="hog")

# the movie returned from the user query
print("=====================")
print("=======RESULTS=======")
print("=====================")
for k, v in movie.items():
    print(f"{k}: {v}")

# print the YouTube video list
for k, v in youtube_videos.items():
    print(f"{k}: {v}")

