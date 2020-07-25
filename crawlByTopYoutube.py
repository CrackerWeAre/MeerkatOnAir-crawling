from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import time
import json
import pymongo

from pymongo import MongoClient
from requests_utils import *
from datetime import datetime

class GetListByTop():

  def __init__(self):
    self.DEVELOPER_KEY = "AIzaSyATi0yW-mcW9vCxMwg0fqOmbkANkKODm3Q"
    self.YOUTUBE_API_SERVICE_NAME = "youtube"
    self.YOUTUBE_API_VERSION = "v3"

  def yotubeByTop(self, options):
    youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
      developerKey=self.DEVELOPER_KEY)
    
    channelIDs = []
    regionCodes = []
    nextPageToken = ""
    while len(channelIDs) <= options.max_results:
      search_response = youtube.search().list(
        part="id,snippet",
        eventType="live",
        type="video",
        order="viewCount",
        pageToken=nextPageToken,
        maxResults=options.per_results
      ).execute()

      nextPageToken = search_response.get("nextPageToken")

      regionCodes.append(search_response.get("regionCode"))
      for search_result in search_response.get("items"):
        channelIDs += [(search_result["snippet"]["channelId"], search_result['snippet']['channelTitle'])]

    channelIDs = [(*info[0],info[1].lower()) for info in zip(channelIDs, regionCodes)]
    return channelIDs

def getTarget(args):
    crl = GetListByTop()
    try:
      return crl.yotubeByTop(args)
    except HttpError as e:
      print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

def insertTargetToMongo(mongo_auth, channelIDs):
    conn = MongoClient('mongodb://%s:%s@%s:%s' % (mongo_auth['username'], mongo_auth['password'], mongo_auth['hostname'], mongo_auth['port']),
                       connect=False)
    db = conn['meerkatonair']
    collection = db['live_list']
    platform = 'youtube'

    for channelID, channel, language in channelIDs:
        res = collection.find({"_uniq": platform + channelID})
        if len([r for r in res]) == 0:
            post_id = collection.insert_one(
                {"_uniq": platform + channelID,
                "channel": channel,
                "channelID": channelID,
                "platform": platform,
                "language": language,
                "updateDate": datetime.now().ctime()})
            print(platform.upper(), channelID, 'UPDATED')

    conn.close()

if __name__ == "__main__":
  argparser.add_argument("--max-results", help="Max results", default=200)
  argparser.add_argument("--per-results", help="per results", default=50)
  args = argparser.parse_args()

  with open('mongodb_auth.json', 'r') as f:
    mongo_auth = json.load(f)

  channelIDs = getTarget(args)
  insertTargetToMongo(mongo_auth, channelIDs)