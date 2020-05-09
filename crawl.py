from bs4 import BeautifulSoup
import requests
import json
import time
from datetime import datetime

import pymongo
from pymongo import MongoClient 
from requests_utils import platform_headers

class LiveCrawling():

    def __init__(self):
        self.platform = None
        self.channel = None
        self.channelID = None
        self.dataset = {}

        with open('mongodb_auth.json', 'r') as f:
            self.mongo_auth = json.load(f)

        self.conn = MongoClient('mongodb://%s:%s@%s:%s' % (self.mongo_auth['username'], self.mongo_auth['password'], self.mongo_auth['hostname'], self.mongo_auth['port']))

        self.db_admin = self.conn['admin']
        collection = self.db_admin['authorization']
        self.auth = collection.find_one()

    def crawl_target(self):
        db = self.conn['meerkatonair']
        collection = db['crawl_target']
        return collection.find()

    def mongo_insert(self):
        db = self.conn['meerkatonair']
        collection = db['live_list']

        # insert
        try:
            if self.dataset != {}:
                post_id = collection.insert_one(self.dataset)
        # update
        except pymongo.errors.DuplicateKeyError:
            post_id = collection.update_one({'_id': self.dataset['_id']}, {"$set": self.dataset}, upsert=True)

        print(self.channel, 'Done')

    def crawling(self):
        for target in self.crawl_target():
            self.dataset = {}
            self.platform = target['platform']
            self.channelID = target['channelID']
            self.channel = target['channel']
  
            if self.platform == 'youtube':
                self.youtube()
            elif self.platform == 'twitch':
                self.twitch()
            elif self.platform == 'afreecatv':
                self.afreecatv()
            else:
                print(self.platform, self.channelID)
                print("Platform undefined")
                continue

            self.mongo_insert()

    def youtube(self):

        url, _ = platform_headers(self.platform, self.channelID)
        urldata = requests.get(url + '/channel/' + self.channelID)

        if urldata.status_code == 200:
            soup = BeautifulSoup(urldata.text, 'html.parser')
            link = soup.select('div.yt-lockup-dismissable')
            linkData =  link[0].select('div.yt-lockup-content')
            dataLiveConfirm = linkData[0].select_one('a')['data-sessionlink']

            if dataLiveConfirm.find('live') > 0 :
                liveData = link[0].select_one('div.yt-lockup-content > h3 > a')
                AttdData = link[0].select_one('div.yt-lockup-content > div.yt-lockup-meta > ul > li ')
                creatorData = link[0].select_one('div.yt-lockup-content > div.yt-lockup-byline > a')

                self.dataset['_id'] = self.channelID

                self.dataset['channel'] = self.channel
                self.dataset['channelID'] = self.channelID
                self.dataset['platform'] = self.platform
                self.dataset['creatorDataHref'] = url + creatorData.attrs['href']
                self.dataset['creatorDataName'] = creatorData.text

                self.dataset['onLive'] = True
                self.dataset['updateDate'] = datetime.now().ctime()
                
                self.dataset['imgDataSrc'] = link[0].select_one('div.yt-lockup-thumbnail > span > a > span > span > span > img').attrs['data-thumb']
                self.dataset['liveDataHref'] = url + liveData.attrs['href']
                self.dataset['liveDataTitle'] = liveData.attrs['title']
                self.dataset['liveAttdc'] = AttdData.text.partition('명')[0]
            else :
                creatorData = link[0].select_one('div.yt-lockup-content > div.yt-lockup-byline > a')

                self.dataset['_id'] = self.channelID

                self.dataset['channel'] = self.channel
                self.dataset['channelID'] = self.channelID
                self.dataset['platform'] = self.platform
                # self.dataset['creatorDataHref'] = url + creatorData.attrs['href']
                # self.dataset['creatorDataName'] = creatorData.text

                self.dataset['onLive'] = False
                self.dataset['updateDate'] = datetime.now().ctime()
        else:
            print('[{}]'.format(urldata.status_code))

    def twitch(self):

        url, headers = platform_headers(self.platform, self.channelID, auth = self.auth)
        urldata = requests.get(url + self.channelID, headers=headers)

        if urldata.status_code == 200:
            urlJsonData = json.loads(urldata.text)

            if urlJsonData != {'data': [], 'pagination': {}} :
                self.dataset['_id'] = self.channelID

                self.dataset['channel'] = self.channel
                self.dataset['channelID'] = self.channel
                self.dataset['platform'] = self.platform
                self.dataset['creatorDataHref'] = "http://twitch.tv/" + self.channelID
                self.dataset['creatorDataName'] = urlJsonData['data'][0]['user_name']

                self.dataset['onLive'] = True
                self.dataset['updateDate'] = datetime.now().ctime()

                self.dataset['imgDataSrc'] = urlJsonData['data'][0]['thumbnail_url'].replace('{width}', '1600').replace('{height}', '900')
                self.dataset['liveDataHref'] = "http://twitch.tv/" + self.channelID
                self.dataset['liveDataTitle'] = urlJsonData['data'][0]['title']
                self.dataset['liveAttdc'] = urlJsonData['data'][0]['viewer_count']
            else :
                self.dataset['_id'] = self.channelID

                self.dataset['channel'] = self.channel
                self.dataset['channelID'] = self.channel
                self.dataset['platform'] = self.platform
                # self.dataset['creatorDataHref'] = "http://twitch.tv/" + self.channelID
                # self.dataset['creatorDataName'] = urlJsonData['data'][0]['user_name']

                self.dataset['onLive'] = False
                self.dataset['updateDate'] = datetime.now().ctime()
        else:
            print('[{}]'.format(urldata.status_code))

    def afreecatv(self):
        
        url, headers = platform_headers(self.platform, self.channelID)
        urldata = requests.get(url, headers=headers)

        if urldata.status_code == 200:
            urlJsonData=json.loads(urldata.text)

            if urlJsonData['broad']:
                self.dataset['_id'] = self.channelID

                self.dataset['channel'] = self.channel
                self.dataset['platform'] = self.platform
                self.dataset['channelID'] = self.channel
                self.dataset['creatorDataHref'] = "http://bj.afreecatv.com/" + self.channelID
                self.dataset['creatorDataName'] = urlJsonData['station']['user_nick']

                self.dataset['onLive'] = True
                self.dataset['updateDate'] = datetime.now().ctime()

                self.dataset['imgDataSrc'] = "liveimg.afreecatv.com/" + str(urlJsonData['broad']['broad_no']) + ".gif"
                self.dataset['liveDataHref'] = "http://play.afreecatv.com/" + self.channelID + "/" + str(urlJsonData['broad']['broad_no'])
                self.dataset['liveDataTitle'] = urlJsonData['broad']['broad_title']
                self.dataset['liveAttdc'] = urlJsonData['broad']['current_sum_viewer']

            else :
                self.dataset['_id'] = self.channelID

                self.dataset['channel'] = self.channel
                self.dataset['platform'] = self.platform
                self.dataset['channelID'] = self.channel
                # self.dataset['creatorDataHref'] = "http://bj.afreecatv.com/" + self.channelID
                # self.dataset['creatorDataName'] = urlJsonData['station']['user_nick']

                self.dataset['onLive'] = False
                self.dataset['updateDate'] = datetime.now().ctime()
        else:
            print('[{}]'.format(urldata.status_code))


if __name__ == '__main__':
    
    crl = LiveCrawling()
    crl.crawling()
