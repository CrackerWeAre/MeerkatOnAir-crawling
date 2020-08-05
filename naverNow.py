import requests
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient 

mongo_auth = {
    "username" : "admin",
    "password" : "pwdtlchd50wh",
    "hostname" : "49.247.134.77",
    "port" : "27017"
}

url = "https://now.naver.com/api/nnow/v1/stream/lineup/"

res = requests.get(url)

item = res.json()

conn = MongoClient('mongodb://%s:%s@%s:%s' % (mongo_auth['username'], mongo_auth['password'], mongo_auth['hostname'], mongo_auth['port']), connect=False)
db = conn['meerkatonair']
collection = db['schedule_list']

collection.delete_many({"platform":"navernow"})

days = ['월', '화', '수', '목', '금', '토', '일', '주 7일', '휴일']

for i in range(0,len(item["contentList"])):
    for j in item["contentList"][i]['lineups']:
        data = {}
        data['_uniq']="navernow"+j['id']
        data['channel']=j['texts']['name']
        data['channelID']= str(j['id'])
        data['title']=j['texts']['name']
        data['description']=j['texts']['big']
        data['image']=j['images']['back']
        data['url']="https://now.naver.com/"+j['id']
        data['category']=item["contentList"][i]['tag']
        data['platform']='navernow'
        data['regular']=True
        
        date = j['texts']['small']
        m = ['오전','오후']
        
        if any(x in date for x in m):
            if m[0] in date:
                apm = m[0]
            else: apm = m[1]
            
            fromTo = date[:date.index(apm)].strip()
            fromToList = list(fromTo)
            
            # 월
            if len(fromToList) == 1:
                data['days'] = fromToList
            # 월-금
            elif fromToList[1] == '-':
                data['days'] = days[days.index(fromToList[0]):days.index(fromToList[-1])+1]
            # 월,화,수
            elif fromToList[1] == ',':
                data['days'] = fromTo.split(',')
            # 휴일
            elif days[-1] in date:
                data['days'] = days[5:7]
            # 주 7일 오후 10시
            elif days[-2] in date:
                data['days'] = days[:7]
            
            
            time = date.split(apm)[-1].strip()
            if '반' in time:
                time = time.replace('시 반',':30')
            elif '분' in time:
                time = time.replace('시 ',':').replace('분','')
            else:
                time = time.replace('시',':00')
            
            if apm == '오후':
                timeList = time.split(':')
                timeList[0] = str(int(timeList[0]) + 12)
                time = ':'.join(timeList)            
        
        else:
            # 주 7일 24시간
            data['days'] = days[:7]
            time = "00:00"
            
        data['hours'] = time
        data['year'] = 2020
        data['month'] = 0
        data['day'] = 0
        collection.insert_one(data)