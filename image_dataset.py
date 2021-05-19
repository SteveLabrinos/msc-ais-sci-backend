"""
    File name: image_dataset.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 18/5/2021
    Date last modified: 19/5/2021
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


def create_image_dataset(actor):
    dir_path = "./dataset/actors/" + str(actor).lower().replace(" ", "_")
    try:
        os.makedirs(dir_path)
    except OSError as e:
        print(f"[Error] Creating of the directory {dir_path} failed")
        print(e)
    else:
        # set the headers and search parameters
        headers = {"Ocp-Apim-Subscription-Key": BING_IMAGE_API}
        params = {"q": actor, "offset": 0, "count": GROUP_SIZE}
        # make the search
        print("[INFO] searching Bing API for '{}'".format(actor))
        search = requests.get(URL, headers=headers, params=params)
        search.raise_for_status()
        # grab the results from the search, including the total number of
        # estimated results returned by the Bing API
        results = search.json()
        est_num_results = min(results["totalEstimatedMatches"], MAX_RESULTS)
        print("[INFO] {} total results for '{}'".format(est_num_results, actor))
        # initialize the total number of images downloaded thus far
        total = 0

        # loop over the estimated number of results in `GROUP_SIZE` groups
        for offset in range(0, est_num_results, GROUP_SIZE):
            # update the search parameters using the current offset, then
            # make the request to fetch the results
            print("[INFO] making request for group {}-{} of {}...".format(
                offset, offset + GROUP_SIZE, est_num_results))
            params["offset"] = offset
            search = requests.get(URL, headers=headers, params=params)
            search.raise_for_status()
            results = search.json()
            print("[INFO] saving images for group {}-{} of {}...".format(
                offset, offset + GROUP_SIZE, est_num_results))

            # loop over the results
            for v in results["value"]:
                # try to download the image
                try:
                    # make a request to download the image
                    print("[INFO] fetching: {}".format(v["contentUrl"]))
                    r = requests.get(v["contentUrl"], timeout=30)
                    # build the path to the output image
                    ext = v["contentUrl"][v["contentUrl"].rfind("."):]
                    p = os.path.sep.join([dir_path, "{}{}".format(
                        str(total).zfill(8), ext)])
                    # write the image to disk
                    f = open(p, "wb")
                    f.write(r.content)
                    f.close()
                    # try to load the image from disk
                    image = cv2.imread(p)
                    # if the image is `None` then we could not properly load the
                    # image from disk (so it should be ignored)
                    if image is None:
                        print("[INFO] deleting: {}".format(p))
                        os.remove(p)
                        continue
                    # update the counter
                    total += 1
                # catch any errors
                except Exception as e:
                    # check to see if our exception is in the list of exceptions
                    if type(e) in EXCEPTIONS:
                        print("[INFO] skipping: {}".format(v["contentUrl"]))
                        continue
