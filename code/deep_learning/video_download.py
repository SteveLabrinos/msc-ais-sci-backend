"""
    File name: execution_in_sequence.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 19/5/2021
    Date last modified: 20/5/2021
    Python Version: 3.8
"""

# download all the videos contained in the list
# from YouTube and store them in the movie dataset

import os
import youtube_dl

BASE_URL = "https://www.youtube.com/watch?v="


def download_youtube_list(movie: str, video_ids: list):
    video_path = f"./dataset/movies/{movie}/videos"
    ydl_opts = {
        'outtmpl': video_path + '/%(id)s.%(ext)s',
    }

    try:
        os.makedirs(video_path)
    except OSError as e:
        print(f"[Error] {e}")

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        for video_id in video_ids:
            try:
                ydl.download([BASE_URL + video_id])
            except Exception as e:
                print(f"[ERROR] {e}")
                continue
