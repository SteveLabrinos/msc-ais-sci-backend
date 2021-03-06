"""
    File name: screen_time.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 20/5/2021
    Date last modified: 20/5/2021
    Python Version: 3.8
"""
from imutils import paths
from code.deep_learning.image_recognition import recognize_faces
import pickle


def video_screen_time(movie: str, video_id: str, model="hog") -> list:
    knowledge_path = f"./encodings/{movie}.pickle"
    # load the known faces and embeddings from the pickle file
    data = pickle.loads(open(knowledge_path, "rb").read())
    # all the frames from the videos
    frame_paths = list(paths.list_images(f"./dataset/movies/{movie}/frames/{video_id}"))

    print(f"[INFO] Starting screen time calculation for {video_id} video - model: {str(model).upper()}")
    actor_screen_time = dict()
    # get the faces and recognize the actors based on the trained model for all the frames
    for frame in frame_paths:
        actors = recognize_faces(data, frame, model=model)
        # calculate actors screen time based on the different frames recognized
        # because the program extracts one frame per second
        for actor in actors:
            actor_screen_time[actor] = actor_screen_time.get(actor, 0) + 1

    print(f"[INFO] screen times for video {video_id} completed")

    return [(lambda k, v: {'id': k, 'duration': v})(k, v) for k, v in actor_screen_time.items()]


def get_screen_time(movie: str, total_videos: int, model="hog") -> list:

    return [video_screen_time(movie, f"v_{v}", model=model) for v in range(total_videos)]

