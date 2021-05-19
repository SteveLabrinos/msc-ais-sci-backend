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


def produce_video_frames(movie: str, video):
    frames_path = "./dataset/movies/" + movie + "/frames"
    video_path = "./dataset/movies/" + movie + "/videos"

    try:
        os.makedirs("./dataset/movies/" + movie + "/frames")
    except OSError as e:
        print(f"[Error] Creating of the directory {movie} failed")
        print(e)
    else:
        cnt = 0
        # capturing the video from the given path
        capture = cv2.VideoCapture(os.path.join(video_path, video))
        # get the frame rate of the input video
        frame_rate = capture.get(cv2.CAP_PROP_FPS)

        while capture.isOpened():
            # getting the current position
            # frame_id = capture.get(cv2.CAP_PROP_POS_MSEC)
            frame_id = capture.get(1)
            ret, frame = capture.read()
            if not ret:
                break
            # get 1 fps to calculate screen time per second
            # with the less possible frames needed
            # opting for performance
            if frame_id % math.floor(frame_rate) == 0:
                file_name = f"{video}_fr{str(cnt).zfill(4)}.jpg"
                cnt += 1
                # cv2.imwrite(".dataset/movies/" + movie + "/frames/" + file_name, frame)
                # frame_path = "./dataset/movies/" + movie + "/frames"
                cv2.imwrite(os.path.join(frames_path, file_name), frame)
        capture.release()
        print(f"[INFO] video {video_path} converted to {cnt} frames")
