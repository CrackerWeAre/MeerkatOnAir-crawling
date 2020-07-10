import json
from pymongo import MongoClient 
import pymysql

with open('mongodb_auth.json', 'r') as f:
    mongo_auth = json.load(f)

conn = MongoClient('mongodb://%s:%s@%s:%s' % (mongo_auth['username'], mongo_auth['password'], mongo_auth['hostname'], mongo_auth['port']),
            connect=False)
db = conn['meerkatonair']
collection = db['live_list']
conn.close()

streamer_list = [(data['channelID'], data['platform']) for data in collection.find({},{ "channelID": 1, "channel": 1, "platform": 1 })]

db = pymysql.connect(host='49.247.134.77', port=3306, user='sparker',passwd='tlchd50wh!', db='mkoa',charset='utf8')
cur = db.cursor()

sql = """insert into streamer_list(channelID, platform)
         values (%s, %s)"""
         
cur.executemany(sql, tuple(streamer_list))
db.commit()