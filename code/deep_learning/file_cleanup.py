"""
    File name: file_cleanup.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 30/5/2021
    Date last modified: 30/5/2021
    Python Version: 3.8
"""

import os
import shutil


# erase all the files that were produced during screen calculation
# in order to save disk space
def erase_files(movie_id: str):
    # remove the encodings of the actors
    encodings_path = f'./encodings'
    remove_dir(encodings_path)

    # remove the actors dataset
    movie_actors_dataset_dir = f'./dataset/actors/{movie_id}'
    remove_dir(movie_actors_dataset_dir)

    # remove the movie's videos and frames
    movie_dir = f'./dataset/movies/{movie_id}'
    remove_dir(movie_dir)


def remove_dir(dir_path: str):
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print(f"[ERROR] Can't delete directory {dir_path}")


def remove_file(file_path: str):
    os.remove(file_path) if os.path.exists(file_path) else print(f"[ERROR] No encodings in {file_path}")

