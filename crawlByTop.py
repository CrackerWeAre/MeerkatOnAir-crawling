import requests
import json
import pymongo
import itertools
from pymongo import MongoClient
from requests_utils import *
from datetime import datetime


class GetListByTop():

    def __init__(self):
        self.auth = self.init_connection()

    def init_connection(self):
        with open('mongodb_auth.json', 'r') as f:
            mongo_auth = json.load(f)

        conn = MongoClient('mongodb://%s:%s@%s:%s' % (mongo_auth['username'], mongo_auth['password'], mongo_auth['hostname'], mongo_auth['port']),
                           connect=False)

        db_admin = conn['admin']
        collection = db_admin['authorization']
        conn.close()
        return collection.find_one()

    def twitchByTop(self):
        _, headers = platform_headers(platform='twitch', auth=self.auth)
        max_results = 200
        first = 50
        user_ids = []
        channelIDs = []
        pagination = ''

        while (len(user_ids) < max_results - 1):
            responseTwitch = requests.get("https://api.twitch.tv/helix/streams", params={
                "first": first,
                "after": pagination,
            }, headers=headers)

            user_ids += [data['user_id'] for data in responseTwitch.json()['data']]
            
            pagination = responseTwitch.json()['pagination']['cursor']

        for i in range(0, len(user_ids), 50):
            responseTwitch = requests.get("https://api.twitch.tv/helix/users", params={
                "id": user_ids[i:i+50],
            }, headers=headers)

            channelIDs += [(data['login'], data['display_name']) for data in responseTwitch.json()['data']]

        return channelIDs

def getTarget():
    crl = GetListByTop()
    return crl.twitchByTop()

def insertTargetToMongo(mongo_auth, results):
    conn = MongoClient('mongodb://%s:%s@%s:%s' % (mongo_auth['username'], mongo_auth['password'], mongo_auth['hostname'], mongo_auth['port']),
                       connect=False)
    db = conn['meerkatonair']
    collection = db['live_list']
    platform = 'twitch'

    for channelID, channel in channelIDs:
        res = collection.find({"_uniq": platform + channelID})
        if len([r for r in res]) == 0:
            post_id = collection.insert_one(
                {"_uniq": platform + channelID,
                "channel": channel,
                "channelID": channelID,
                "platform": platform,
                "updateDate": datetime.now().ctime()})
            print(platform.upper(), channelID, 'UPDATED')

    conn.close()

if __name__ == '__main__':

    with open('mongodb_auth.json', 'r') as f:
        mongo_auth = json.load(f)

    channelIDs = getTarget()
    insertTargetToMongo(mongo_auth, channelIDs)
