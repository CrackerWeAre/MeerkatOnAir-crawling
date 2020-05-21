import requests
import json
import time
import pymongo

from datetime import datetime
from bs4 import BeautifulSoup
from pymongo import MongoClient 
from requests_utils import *
from selenium import webdriver
from multiprocessing import Pool

class LiveCrawling():

    def __init__(self, debug=False):
        self.platform = None
        self.channel = None
        self.channelID = None
        self.debug = debug
        self.dataset = {}
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
       
        with open('mongodb_auth.json', 'r') as f:
            self.mongo_auth = json.load(f)

        self.conn = MongoClient('mongodb://%s:%s@%s:%s' % (self.mongo_auth['username'], self.mongo_auth['password'], self.mongo_auth['hostname'], self.mongo_auth['port']),
                    connect=False)

        self.db_admin = self.conn['admin']
        collection = self.db_admin['authorization']
        self.auth = collection.find_one()

    # webdriver는 single-thread 라서 __init__에 있으면 multiprocessing 오류가 뜸.
    # process별로 개별 생성해야한다.
    def init_webdriver(self):
        driver = webdriver.Chrome('driver/chromedriver', options=self.options)
        return driver

    def close_webdriver(self, driver):
        driver.quit()

    def mongo_insert(self):
        db = self.conn['meerkatonair']
        collection = db['live_list']

        # insert
        try:
            if self.dataset != {}:
                post_id = collection.insert_one(self.dataset)
        # update
        except pymongo.errors.DuplicateKeyError:
            post_id = collection.update_one({'_uniq': self.platform + self.channelID}, {"$set": self.dataset})
        # print(self.platform, self.channel, 'Done', self.dataset['updateDate'])

    def crawling(self, target):
        target = {k:v for k,v in target}
        self.dataset = {}
        try:
            self.platform = target['platform']
            self.channelID = target['channelID']
            self.channel = target['channel']

            if self.platform == 'youtube':
                self.youtube()
            elif self.platform == 'twitch':
                self.twitch()
            elif self.platform == 'afreecatv':
                self.afreecatv()
            elif self.platform == 'vlive':        
                pass        
                #self.vlive()
            else:
                print(self.platform, self.channelID, "Platform undefined")

            if not self.debug:
                self.mongo_insert()
        
        except Exception as e:
            print(self.platform, self.channel, 'Error', e)
            
    def vlive(self):

        url, _ = platform_headers(self.platform, self.channelID)

        driver = self.init_webdriver()
        driver.get(url)
        time.sleep(0.6)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        if not soup.select_one('.onair') == None:
            
            self.dataset['_uniq'] = self.platform + self.channelID

            self.dataset['channel'] = self.channel
            self.dataset['channelID'] = self.channelID
            self.dataset['platform'] = self.platform

            self.dataset['creatorDataHref'] = url
            self.dataset['creatorDataName'] = soup.select_one('.channel_info_area .name').text

            self.dataset['onLive'] = True
            self.dataset['updateDate'] = datetime.now().ctime()

            src = soup.select_one('.onair .article_link .article_img img')['src']
            self.dataset['imgDataSrc'] = replace_ascii(src).split('src="')[-1].split('"&')[0]
            self.dataset['liveDataHref'] = soup.select_one('.onair .article_link')['href']
            self.dataset['liveDataTitle'] = soup.select_one('.onair .article_link .title').text
            self.dataset['liveAttdc'] = int(soup.select_one('.onair .article_link .info.chat').text.replace('chat count','').replace('K','000'))
        else:
            self.dataset['_uniq'] = self.platform + self.channelID

            self.dataset['channel'] = self.channel
            self.dataset['platform'] = self.platform
            self.dataset['channelID'] = self.channelID

            self.dataset['onLive'] = False
            self.dataset['updateDate'] = datetime.now().ctime()
            
        self.close_webdriver(driver)

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

                self.dataset['_uniq'] = self.platform + self.channelID

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
                self.dataset['liveAttdc'] = int(AttdData.text.partition('명')[0].replace(',',''))
            else :
                creatorData = link[0].select_one('div.yt-lockup-content > div.yt-lockup-byline > a')

                self.dataset['_uniq'] = self.platform + self.channelID

                self.dataset['channel'] = self.channel
                self.dataset['channelID'] = self.channelID
                self.dataset['platform'] = self.platform

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
                self.dataset['_uniq'] = self.platform + self.channelID

                self.dataset['channel'] = self.channel
                self.dataset['channelID'] = self.channelID
                self.dataset['platform'] = self.platform
                self.dataset['creatorDataHref'] = "http://twitch.tv/" + self.channelID
                self.dataset['creatorDataName'] = urlJsonData['data'][0]['user_name']

                self.dataset['onLive'] = True
                self.dataset['updateDate'] = datetime.now().ctime()

                self.dataset['imgDataSrc'] = urlJsonData['data'][0]['thumbnail_url'].replace('{width}', '250').replace('{height}', '140')
                self.dataset['liveDataHref'] = "http://twitch.tv/" + self.channelID
                self.dataset['liveDataTitle'] = urlJsonData['data'][0]['title']
                self.dataset['liveAttdc'] = urlJsonData['data'][0]['viewer_count']

                self.dataset['category'], self.dataset['detail'] = parse_category(self.platform, urlJsonData['data'][0]['game_id'], headers=headers)
            else :
                self.dataset['_uniq'] = self.platform + self.channelID

                self.dataset['channel'] = self.channel
                self.dataset['channelID'] = self.channelID
                self.dataset['platform'] = self.platform

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
                self.dataset['_uniq'] = self.platform + self.channelID

                self.dataset['channel'] = self.channel
                self.dataset['platform'] = self.platform
                self.dataset['channelID'] = self.channel
                self.dataset['creatorDataHref'] = "http://bj.afreecatv.com/" + self.channelID
                self.dataset['creatorDataName'] = urlJsonData['station']['user_nick']

                self.dataset['onLive'] = True
                self.dataset['updateDate'] = datetime.now().ctime()
                self.dataset['imgDataSrc'] = "//liveimg.afreecatv.com/" + str(urlJsonData['broad']['broad_no']) + ".gif"
                self.dataset['liveDataHref'] = "http://play.afreecatv.com/" + self.channelID + "/" + str(urlJsonData['broad']['broad_no'])
                self.dataset['liveDataTitle'] = urlJsonData['broad']['broad_title']
                self.dataset['liveAttdc'] = urlJsonData['broad']['current_sum_viewer']

            else :
                self.dataset['_uniq'] = self.platform + self.channelID

                self.dataset['channel'] = self.channel
                self.dataset['platform'] = self.platform
                self.dataset['channelID'] = self.channel

                self.dataset['onLive'] = False
                self.dataset['updateDate'] = datetime.now().ctime()
        else:
            print('[{}]'.format(urldata.status_code))

def process(target):
    crl = LiveCrawling(debug=False)
    crl.crawling(target=target)

def crawl_target(mongo_auth):
    
    conn = MongoClient('mongodb://%s:%s@%s:%s' % (mongo_auth['username'], mongo_auth['password'], mongo_auth['hostname'], mongo_auth['port']),
                connect=False)
    db = conn['meerkatonair']
    collection = db['crawl_target']
    conn.close()
    return collection.find()

if __name__ == '__main__':

    with open('mongodb_auth.json', 'r') as f:
        mongo_auth = json.load(f)
    
    target = crawl_target(mongo_auth)
    pool = Pool(processes=16)

    t = [list(i.items()) for i in list(target)]

    s = time.time()    
    pool.map(process,t)
    print('Total : ', time.time() -s)
