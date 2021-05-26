"""
    File name: execution_in_sequence.py
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

TOP_CAST_SIZE = 3
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

        # final movie information from the IMDb API
        m_title = best_match["title"] if "title" in best_match else "Non Available"
        m_img = best_match["image"]["url"] if "image" in best_match else "Non Available"
        m_year = best_match["year"] if "year" in best_match else "Non Available"
        m_type = best_match["titleType"] if "titleType" in best_match else "Non Available"

        movie = {
            "id": movie_id,
            "title": m_title,
            "type": m_type,
            "image_url": m_img,
            "year": m_year,
        }

        print(f"[INFO] Movie search completed - movie returned: {movie['title']}")
        return movie


# search for the 4 top cast of the movie based on the movie ID
def get_cast(movie_id: str):
    cast_url = BASE_URL + "/get-top-cast"
    top_cast_id = imdb_request({"tconst": movie_id}, cast_url)[0:TOP_CAST_SIZE]

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
        name = cast[actor_id]["name"]["name"] if "name" in cast[actor_id] else "Not available"
        image = cast[actor_id]["name"]["image"]["url"] if "image" in cast[actor_id]["name"] else "Not available"
        role = cast[actor_id]["charname"][0]["characters"][0] if "charname" in cast[actor_id] else "Not available"
        char_list.append({
            "id": actor_id,
            "name": name,
            "image": image,
            "role_name": role
        })

    return char_list

