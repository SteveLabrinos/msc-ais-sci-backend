"""
    File name: image_dataset.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 18/5/2021
    Date last modified: 25/5/2021
    Python Version: 3.8
"""

from requests import exceptions
from api_keys import BING_IMAGE_API
import requests
import cv2
import os

MAX_RESULTS = 20
GROUP_SIZE = 10

URL = "https://api.bing.microsoft.com/v7.0/images/search"

# exceptions that can be thrown
EXCEPTIONS = {IOError, FileNotFoundError, exceptions.RequestException,
              exceptions.HTTPError, exceptions.ConnectionError,
              exceptions.Timeout}


def create_image_dataset(actor, movie, num_of_results=MAX_RESULTS):
    dir_path = f"./dataset/actors/{movie.id}/{actor.id}"
    try:
        os.makedirs(dir_path)
    except OSError as e:
        print(f"[Error] Creating of the directory {dir_path} failed - {e}")
    else:
        group_size = min(GROUP_SIZE, num_of_results)
        # set the headers and search parameters
        headers = {"Ocp-Apim-Subscription-Key": BING_IMAGE_API}
        query = f"{actor.name} - {movie.title}"
        params = {"q": query, "offset": 0, "count": group_size}
        # make the search
        print(f"[INFO] searching Bing API for '{query}'")
        search = requests.get(URL, headers=headers, params=params)
        search.raise_for_status()
        # grab the images from the search, including the total number of
        # estimated images returned by the Bing API
        results = search.json()
        est_num_results = min(results["totalEstimatedMatches"], num_of_results)
        print(f"[INFO] {est_num_results} total images for '{query}'")
        # initialize the total number of images downloaded thus far
        total = 0

        # loop over the estimated number of images in `GROUP_SIZE` groups
        for offset in range(0, est_num_results, group_size):
            # update the search parameters using the current offset, then
            # make the request to fetch the images
            print(f"[INFO] making request for group {offset}-{offset + group_size} of {est_num_results}...")
            params["offset"] = offset
            search = requests.get(URL, headers=headers, params=params)
            search.raise_for_status()
            results = search.json()
            print(f"[INFO] saving images for group {offset}-{offset + group_size} of {est_num_results}...")

            # loop over the images
            for value in results["value"]:
                # download the image
                try:
                    print(f"[INFO] fetching: {value['contentUrl']}")
                    request = requests.get(value["contentUrl"], timeout=30)
                    # build the path to the output image
                    file_extension = value["contentUrl"][value["contentUrl"].rfind("."):]
                    path = os.path.sep.join([dir_path, f"{str(total).zfill(8)}{file_extension}"])
                    # write the image to disk
                    file = open(path, "wb")
                    file.write(request.content)
                    file.close()
                    # try to load the image from disk
                    image = cv2.imread(path)
                    # if the image is `None` then we could not properly load the
                    # image from disk
                    if image is None:
                        print(f"[INFO] deleting: {path}")
                        os.remove(path)
                        continue
                    total += 1
                except Exception as e:
                    if type(e) in EXCEPTIONS:
                        print(f"[INFO] skipping: {value['contentUrl']}")
                        continue
