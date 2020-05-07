from bs4 import BeautifulSoup
import requests
import json
import time
from datetime import datetime

import pymongo
from pymongo import MongoClient 
from requests_utils import platform_headers

class LiveCrawling():

    def __init__(self, platform = None, channelID = None):
        self.platform = platform
        self.channelID = channelID
        self.dataset = {}

        with open('littleproject/mongodb_auth.json', 'r') as f:
            self.mongo_auth = json.load(f)

        self.conn = MongoClient('mongodb://%s:%s@%s:%s' % (self.mongo_auth['username'], self.mongo_auth['password'], self.mongo_auth['hostname'], self.mongo_auth['port']))

    def target_crawl(self):
        db = self.conn['moadata']
        collection = db['crawl_target']
        return collection.find_one()

    def mongo_insert(self):

        db = self.conn['moadata']
        collection = db['moadata']

        # insert
        try:
            if self.dataset != {}:
                post_id = collection.insert_one(self.dataset)
        # update
        except pymongo.errors.DuplicateKeyError:
            post_id = collection.update_one({'_id': self.dataset['_id']}, {"$set": self.dataset}, upsert=True)

        for d in collection.find():
            print(d)

    def crawling(self):
        if self.platform == 'youtube':
            data = self.youtube()
        elif self.platform == 'twitch':
            data = self.twitch()
        elif self.platform == 'afreecatv':
            data = self.afreecatv()
        else:
            print("Platform undefined")
            raise

        return data

    def youtube(self):

        url, _ = platform_headers(self.platform, self.channelID)
        urldata = requests.get(url + '/channel/' + self.channelID)

        if urldata.status_code == 200:
            soup = BeautifulSoup(urldata.text, 'html.parser')
            link = soup.select('div.yt-lockup-dismissable')
            linkData =  link[0].select('div.yt-lockup-content')
            dataLiveConfirm = linkData[0].select_one('a')['data-sessionlink']

            if dataLiveConfirm.find('live') > 0 :
                self.dataset['_id'] = self.channelID
                self.dataset['channelID'] = self.channelID
                self.dataset['imgDataSrc'] = link[0].select_one('div.yt-lockup-thumbnail > span > a > span > span > span > img').attrs['data-thumb']
                
                liveData = link[0].select_one('div.yt-lockup-content > h3 > a')
                self.dataset['liveDataHref'] = url + liveData.attrs['href']
                self.dataset['liveDataTitle'] = liveData.attrs['title']

                creatorData = link[0].select_one('div.yt-lockup-content > div.yt-lockup-byline > a')
                self.dataset['creatorDataHref'] = url + creatorData.attrs['href']
                self.dataset['creatorDataName'] = creatorData.text

                AttdData = link[0].select_one('div.yt-lockup-content > div.yt-lockup-meta > ul > li ')
                self.dataset['liveAttdc'] = AttdData.text.partition('명')[0]
                self.dataset['platform'] = self.platform
                self.dataset['onLive'] = True
                self.dataset['date'] = datetime.now().ctime()
            else :
                self.dataset['_id'] = self.channelID
                self.dataset['platform'] = self.platform
                self.dataset['onLive'] = False
                self.dataset['date'] = datetime.now().ctime()
        else:
            print('[{}]'.format(urldata.status_code))

    def twitch(self):
    
        url, headers = platform_headers(self.platform, self.channelID)
        urldata = requests.get(url + self.channelID, headers=headers)

        print(urldata.text)

        if urldata.status_code == 200:
            urlJsonData = json.loads(urldata.text)

            if urlJsonData != {'data': [], 'pagination': {}} :
                self.dataset['_id'] = self.channelID
                self.dataset['channelID'] = urlJsonData['data'][0]['user_id']
                self.dataset['imgDataSrc'] = urlJsonData['data'][0]['thumbnail_url'].replace('{width}', '1600').replace('{height}', '900')
                self.dataset['liveDataHref'] = "http://twitch.tv/" + self.channelID
                self.dataset['liveDataTitle'] = urlJsonData['data'][0]['title']
                self.dataset['creatorDataHref'] = "http://twitch.tv/" + self.channelID
                self.dataset['creatorDataName'] = urlJsonData['data'][0]['user_name']
                self.dataset['liveAttdc'] = urlJsonData['data'][0]['viewer_count']
                self.dataset['platform'] = self.platform
                self.dataset['onLive'] = True
                self.dataset['date'] = datetime.now().ctime()
            else :
                self.dataset['_id'] = self.channelID
                self.dataset['platform'] = self.platform
                self.dataset['onLive'] = False
                self.dataset['date'] = datetime.now().ctime()
        else:
            print('[{}]'.format(urldata.status_code))

    def afreecatv(self):
        
        url, headers = platform_headers(self.platform, self.channelID)
        urldata = requests.get(url, headers=headers)

        if urldata.status_code == 200:
            urlJsonData=json.loads(urldata.text)

            if urlJsonData['broad']:
                self.dataset['_id'] = self.channelID
                self.dataset['imgDataSrc'] = "liveimg.afreecatv.com/" + str(urlJsonData['broad']['broad_no']) + ".gif"
                self.dataset['liveDataHref'] = "http://play.afreecatv.com/" + self.channelID + "/" + str(urlJsonData['broad']['broad_no'])
                self.dataset['liveDataTitle'] = urlJsonData['broad']['broad_title']
                self.dataset['creatorDataHref'] = "http://bj.afreecatv.com/" + self.channelID
                self.dataset['creatorDataName'] = urlJsonData['station']['user_nick']
                self.dataset['liveAttdc'] = urlJsonData['broad']['current_sum_viewer']
                self.dataset['platform'] = self.platform
                self.dataset['date'] = datetime.now().ctime()
            else :
                self.dataset['_id'] = self.channelID
                self.dataset['platform'] = self.platform
                self.dataset['onLive'] = False
                self.dataset['date'] = datetime.now().ctime()
        else:
            print('[{}]'.format(urldata.status_code))


if __name__ == '__main__':
    
    platform = 'youtube'
    channelID = 'UCsOW9TPy2TKkqCchUHL04Fg'

    crl = LiveCrawling(platform = platform, channelID= channelID)
