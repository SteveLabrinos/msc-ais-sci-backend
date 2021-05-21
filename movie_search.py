"""
    File name: app.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 20/5/2021
    Date last modified: 21/5/2021
    Python Version: 3.8
"""

# using RapidAPI to consume IMDb API in order
# to get the title from the users query and the
# top casting actors

import requests
from api_keys import RAPID_API_KEY

RAPID_API_HOST = "imdb8.p.rapidapi.com"
BASE_URL = f"https://{RAPID_API_HOST}/title"

headers = {
    "x-rapidapi-key": RAPID_API_KEY,
    "x-rapidapi-host": RAPID_API_HOST,
    "content-type": 'application/json'
}


def imdb_request(query_string: dict, url: str) -> dict:
    return requests.request(
        "GET", url,
        headers=headers,
        params=query_string,
    ).json()


def get_movie(query_string: str) -> dict:
    movie_url = BASE_URL + "/find"
    response = imdb_request({"q": query_string}, movie_url)

    # ensure that the the api returned data
    if "results" in response:
        best_match = response["results"][0]
        movie_id = best_match["id"][7:-1]

        # search for the 4 top cast of the movie based on the movie ID
        cast_url = BASE_URL + "/get-top-cast"
        top_cast_id = imdb_request({"tconst": movie_id}, cast_url)[0:3]

        # search for cast information based on the name ID and the movie ID
        char_list = list()
        char_url = BASE_URL + "/get-charname-list"
        for cast_id in top_cast_id:
            actor_id = cast_id[6:-1]
            cast = imdb_request({
                "id": actor_id,
                "tconst": movie_id,
                "currentCountry": "US",
                "marketplace": "ATVPDKIKX0DER",
                "purchaseCountry": "US"
            }, char_url)
            # set the actors details and role details
            char_list.append({
                "actor_id": actor_id,
                "actor_name": cast[actor_id]["name"]["name"],
                "actor_image": cast[actor_id]["name"]["image"]["url"],
                "role_name": cast[actor_id]["charname"][0]["characters"][0]
            })

        # final movie information from the IMDb API
        movie = {
            "movie_id": movie_id,
            "movie_title": best_match["title"],
            "movie_type": best_match["titleType"],
            "image_url": best_match["image"]["url"],
            "year": best_match["year"],
            "cast": char_list
        }

        print(f"[INFO] Movie search completed - movie returned: {movie['movie_title']}")
        return movie
