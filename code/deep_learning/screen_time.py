"""
    File name: encode_faces.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 20/5/2021
    Date last modified: 20/5/2021
    Python Version: 3.8
"""
from imutils import paths
from code.deep_learning.image_recognition import recognize_faces


def video_screen_time(movie: str, video_folder: str, knowledge, model="hog") -> dict:
    # all the frames from the videos
    frame_paths = list(paths.list_images(f"./dataset/movies/{movie}/frames/{video_folder}"))

    print(f"[INFO] Starting screen time calculation for {video_folder} video...")
    actor_screen_time = dict()
    # get the faces and recognize the actors based on the trained model for all the frames
    for frame in frame_paths:
        actors = recognize_faces(knowledge, frame, model=model)
        # calculate actors screen time based on the different frames recognized
        # because the program extracts one frame per second
        for actor in actors:
            actor_screen_time[actor] = actor_screen_time.get(actor, 0) + 1

    print(f"[INFO] screen times for video {video_folder} completed")
    return actor_screen_time


def get_screen_time(movie: str, total_videos: int, model="hog") -> list:
    # the trained encoding dataset for the classification model
    encodings = f"./encodings/{movie}.pickle"

    return [video_screen_time(movie, f"v_{v}", encodings, model=model) for v in range(total_videos)]

