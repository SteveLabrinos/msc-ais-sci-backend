"""
    File name: video_search.py
    Author: Steve Labrinos, Konstantinos Raptis
    Date created: 19/5/2021
    Date last modified: 27/5/2021
    Python Version: 3.8
"""

from api_keys import YOU_TUBE_API
from googleapiclient.discovery import build
import isodate

# extract video list based on user search and save them
# under the corresponding movie

# creating the youtube service object
# YouTube API doc:
# https://github.com/googleapis/google-api-python-client/blob/master
youtube = build('youtube', 'v3', developerKey=YOU_TUBE_API)


def youtube_search(query: str, max_results=5, order="relevance"):
    # create a request to search for video list based on end user criteria
    response = youtube.search().list(
        part="id, snippet",
        q=query,
        type="video",
        order=order,
        maxResults=max_results,
        videoDuration="short"
    ).execute()

    print("[INFO] YouTube videos search completed...")
    return response


def deserialize_response(response_data):
    video_list = list()
    for search_result in response_data.get("items", []):
        video_result = dict()

        video_result['id'] = search_result['id']['videoId']
        video_result['title'] = search_result['snippet']['title']

        # collect stats on each video using video_id
        stats = youtube.videos().list(
            part='statistics, contentDetails',
            id=search_result['id']['videoId']).execute()

        video_result['duration_sec'] = isodate.parse_duration(stats['items'][0]['contentDetails']['duration']).seconds
        video_result['view_count'] = stats['items'][0]['statistics']['viewCount']

        # Not every video has likes/dislikes enabled]
        if 'likeCount' in stats['items'][0]['statistics']:
            video_result['like_count'] = stats['items'][0]['statistics']['likeCount']
        else:
            video_result['like_count'] = None

        if 'dislikeCount' in stats['items'][0]['statistics']:
            video_result['dislike_count'] = stats['items'][0]['statistics']['dislikeCount']
        else:
            video_result['dislike_count'] = None

        if 'commentCount' in stats['items'][0]['statistics']:
            video_result['comment_count'] = stats['items'][0]['statistics']['commentCount']
        else:
            video_result['comment_count'] = None

        video_result['image_url'] = search_result['snippet']['thumbnails']['default']['url']

        video_list.append(video_result)

    return video_list
