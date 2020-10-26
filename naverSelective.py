import requests
import json
from datetime import datetime
from pymongo import MongoClient 

mongo_auth = {
    "username" : "admin",
    "password" : "pwdtlchd50wh",
    "hostname" : "49.247.134.77",
    "port" : "27017"
}

conn = MongoClient('mongodb://%s:%s@%s:%s' % (mongo_auth['username'], mongo_auth['password'], mongo_auth['hostname'], mongo_auth['port']), connect=False)
db = conn['meerkatonair']
collection = db['schedule_list']
# collection.delete_many({"platform":"naverselective"})

milestones_url = "https://apis.naver.com/selectiveweb/live_commerce_web/v2/broadcast/milestones"
milestones = requests.get(milestones_url).json()
params = ""

for ms in milestones:
    # 현재 날짜가 3번째에 표시됨
    timestamp = ms['milestone']['timestamp']
    url=f"https://apis.naver.com/selectiveweb/selectiveweb/v1/lives/timeline/daily/?next={timestamp}&size=30"

    data=requests.get(url)
    itemList=json.loads(data.text)

    for i in range(0,len(itemList["list"])):
        data = {}
        data['_uniq']="naverselective"+str(itemList['list'][i]['broadcastId'])
        data['channel']=itemList['list'][i]['urlId']
        data['channelID']=str(itemList['list'][i]['broadcastId'])
        data['title']=itemList['list'][i]['broadcastTitle']
        data['description']=itemList['list'][i]['displayProduct']['name'] if itemList['list'][i]['displayProduct']['name'] else ""
        data['image']=itemList['list'][i]['broadcastBridgeMobileImage']
        data['url']=itemList['list'][i]['broadcastEndUrl']
        data['category']=itemList['list'][i]['serviceName']
        data['platform']="naverselective"
        data['regular']=False
        time = datetime.strptime(itemList['list'][i]['expectedStartDate'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
        if time.minute == 0:
            m = "00"
        else:
            m = "30"
        data['hours']=str(time.hour)+":"+m
        if(time.weekday()==0):
            data['days']=['월']
        elif(time.weekday()==1):
            data['days']=['화']
        elif(time.weekday()==2):
            data['days']=['수']
        elif(time.weekday()==3):
            data['days']=['목']
        elif(time.weekday()==4):
            data['days']=['금']
        elif(time.weekday()==5):
            data['days']=['토']
        elif(time.weekday()==6):
            data['days']=['일']
            
        data['year']=time.year
        data['month']=time.month
        data['day']=time.day
        
        print(data)
        
        collection.insert_one(data)
    