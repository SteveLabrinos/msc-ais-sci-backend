"""
    File name: app.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 19/5/2021
    Date last modified: 19/5/2021
    Python Version: 3.8
"""

from api_keys import YOU_TUBE_API
from googleapiclient.discovery import build

# extract video list based on user search and save them
# under the corresponding movie

# creating the youtube service object
# YouTube API doc:
# https://github.com/googleapis/google-api-python-client/blob/master
youtube = build('youtube', 'v3', developerKey=YOU_TUBE_API)


def youtube_search(query, max_results=5, order="relevance"):
    # create a request to search for video list based on end user criteria
    response = youtube.search().list(
        part="id, snippet",
        q=query,
        type="video",
        order=order,
        maxResults=max_results,
        videoDuration="short"
    ).execute()

    print("[INFO] Search completed...")
    return response


def deserialize_response(response_data):
    # create variables to store your values
    title = []
    view_count = []
    like_count = []
    dislike_count = []
    comment_count = []
    video_id = []

    for search_result in response_data.get("items", []):
        video_id.append(search_result['id']['videoId'])
        title.append(search_result['snippet']['title'])
        # then collect stats on each video using video_id
        stats = youtube.videos().list(
            part='statistics, snippet',
            id=search_result['id']['videoId']).execute()

        view_count.append(stats['items'][0]['statistics']['viewCount'])
        # Not every video has likes/dislikes enabled so they won't appear in JSON response
        try:
            like_count.append(stats['items'][0]['statistics']['likeCount'])
        except FileNotFoundError:
            # Appends "Not Available" to keep dictionary values aligned
            like_count.append("Not available")

        try:
            dislike_count.append(stats['items'][0]['statistics']['dislikeCount'])
        except FileNotFoundError:
            dislike_count.append("Not available")

        try:
            comment_count.append(stats['items'][0]['statistics']['commentCount'])
        except FileNotFoundError:
            comment_count.append("Not available")

    # Break out of for-loop and if statement and store lists of values in dictionary
    youtube_dict = {'title': title, 'video_id': video_id,
                    'view_count': view_count, 'like_count': like_count,
                    'dislike_count': dislike_count, 'comment_count': comment_count}

    return youtube_dict

