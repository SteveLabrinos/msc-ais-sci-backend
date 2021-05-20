"""
    File name: encode_faces.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 20/5/2021
    Date last modified: 20/5/2021
    Python Version: 3.8
"""

# pass a video to extract one frame per second and store it
# in the images directory of the movie dataset
import cv2
import math
import os
from imutils import paths


def process_video_list(movie: str):
    path = "./dataset/movies/" + movie + "/videos"
    videos_path = list(paths.list_files(path))

    for i, video_path in enumerate(videos_path):
        video = video_path.split(os.path.sep)[-1]
        produce_video_frames(movie, video, i)


def produce_video_frames(movie: str, video: str, counter: int):
    # frames_path = "./dataset/movies/" + movie + "/frames"
    frames_path = f"./dataset/movies/{movie}/frames/v_{counter}"
    os.makedirs(frames_path)
    video_path = "./dataset/movies/" + movie + "/videos"

    cnt = 0
    # capturing the video from the given path
    capture = cv2.VideoCapture(os.path.join(video_path, video))
    # get the frame rate of the input video
    frame_rate = capture.get(cv2.CAP_PROP_FPS)

    while capture.isOpened():
        # Relative position of the video file: 0 = start of the film
        # 1 = end of the film
        # frame_id = capture.get(cv2.CAP_PROP_POS_AVI_RATIO)
        frame_id = capture.get(1)
        ret, frame = capture.read()
        if not ret:
            break
        # get 1 fps to calculate screen time per second
        # with the less possible frames needed
        # opting for performance
        if frame_id % math.floor(frame_rate) == 0:
            file_name = f"{str(video).lower().replace(' ', '_')}_fr{str(cnt).zfill(4)}.jpg"
            cnt += 1
            cv2.imwrite(os.path.join(frames_path, file_name), frame)
    capture.release()
    print(f"[INFO] video {video} converted to {cnt} frames")
