from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import time

DEVELOPER_KEY = "AIzaSyATi0yW-mcW9vCxMwg0fqOmbkANkKODm3Q"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
  
  videos = []
  nextPageToken = ""
  while len(videos) <= options.max_results:
    print(len(videos))
    search_response = youtube.search().list(
      part="id,snippet",
      eventType="live",
      type="video",
      pageToken=nextPageToken,
      maxResults=options.per_results
    ).execute()
    time.sleep(0.5)

    nextPageToken = search_response.get("nextPageToken")
    print(nextPageToken)

    for search_result in search_response.get("items", []):
      if search_result["kind"] == "youtube#searchResult":
        if search_result["id"]["kind"] == "youtube#video":
          videos.append(search_result["id"]["videoId"])

  print(videos)
  channels = []
  for i in range(0, len(videos), options.per_results):
    videos_batch = videos[i:i+options.per_results]
    search_video_response = youtube.videos().list(
    part="snippet,statistics,liveStreamingDetails",
    id=",".join(videos_batch),
    maxResults=options.per_results
    ).execute()

    for search_result in search_video_response.get("items",[]):
      if search_result["kind"] == "youtube#video":
        snippet = search_result['snippet']
        statistics = search_result['statistics']
        liveStreamingDetails = search_result['liveStreamingDetails']
        channels.append({
            "channelId" : snippet['channelId'],
            "title" : snippet['title'],
            "description": snippet['description'],
            "thumbnails": snippet['thumbnails'],
            "channelTitle": snippet['channelTitle'],
            "liveBroadcastContent": snippet['liveBroadcastContent'],
            "publishedAt": snippet['publishedAt'],
            # "tags": snippet['tags'],
            "categoryId": snippet['categoryId'],

            "viewCount": statistics['viewCount'],
            "likeCount": statistics['likeCount'],
            "dislikeCount": statistics['dislikeCount'],
            "favoriteCount": statistics['favoriteCount'],
            "commentCount": statistics['commentCount'],

            "actualStartTime": liveStreamingDetails['actualStartTime'],
            # "scheduledStartTime": liveStreamingDetails['scheduledStartTime'],
            "concurrentViewers": liveStreamingDetails['concurrentViewers']
            })

  print(len(videos))
  print(len(channels))

if __name__ == "__main__":
  argparser.add_argument("--max-results", help="Max results", default=10)
  argparser.add_argument("--per-results", help="per results", default=1)
  args = argparser.parse_args()

  try:
    youtube_search(args)
  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))