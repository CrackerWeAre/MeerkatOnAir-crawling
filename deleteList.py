from pymongo import MongoClient

mongo_auth = {
    "username" : "admin",
    "password" : "pwdtlchd50wh",
    "hostname" : "49.247.134.77",
    "port" : "27017"
}

conn = MongoClient('mongodb://%s:%s@%s:%s' % (mongo_auth['username'], mongo_auth['password'], mongo_auth['hostname'], mongo_auth['port']), connect=False)
db = conn['meerkatonair']
collection = db['live_list']

query = {"language": {"$nin":["ko","en","es","kr"]}}

collection.delete_many(query)

