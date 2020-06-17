import requests
import json
import time
import pymongo
import argparse

from datetime import datetime
from bs4 import BeautifulSoup
from pymongo import MongoClient 
from requests_utils import *
from selenium import webdriver
# from pathos.multiprocessing import ProcessingPool as Pool #pip install pathos
from multiprocessing import Pool


class LiveCrawling():

    def __init__(self, browser='chrome'):
        self.platform = None
        self.channel = None
        self.channelID = None
        self.dataset = {}
        self.auth = self.init_connection()

        if browser == 'chrome':
            self.options = webdriver.ChromeOptions()
            self.options.add_argument('--headless')
            self.options.add_argument('--disable-extensions')
            self.options.add_argument('--no-sandbox')
            self.options.add_argument('--disable-dev-shm-usage')
            self.options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    # webdriver는 single-thread 라서 __init__에 있으면 multiprocessing 오류가 뜸.
    # process별로 개별 생성해야한다.
    def init_webdriver(self):
        driver = webdriver.Chrome('driver/chromedriver', options=self.options)
        #driver = webdriver.Chrome('driver/chromedriver.exe', options=self.options)
        return driver

    def init_connection(self):
        with open('mongodb_auth.json', 'r') as f:
            mongo_auth = json.load(f)

        conn = MongoClient('mongodb://%s:%s@%s:%s' % (mongo_auth['username'], mongo_auth['password'], mongo_auth['hostname'], mongo_auth['port']),
                    connect=False)

        db_admin = conn['admin']
        collection = db_admin['authorization']
        conn.close()
        return collection.find_one()

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
                self.vlive()
            else:
                print(self.platform.upper() , self.channelID, "Platform undefined")

            return self.platform, self.channelID, self.dataset
        
        except Exception as e:
            print(self.platform.upper(), self.channelID, 'Error', e)
            
    def vlive(self):
        url, _ = platform_headers(self.platform, self.channelID)
        driver = self.init_webdriver()
        driver.get(url)
        time.sleep(3)
        
        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            if not soup.select_one('.onair') == None:
                
                self.dataset['_uniq'] = self.platform + self.channelID

                self.dataset['channel'] = self.channel
                self.dataset['channelID'] = self.channelID
                self.dataset['platform'] = self.platform

                self.dataset['creatorDataHref'] = url
                self.dataset['creatorDataName'] = soup.select_one('.channel_info_area .name').text
                self.dataset['creatorDataLogo'] = soup.selct_one('img_thumb ng-star-inserted')['src']

                self.dataset['onLive'] = True
                self.dataset['updateDate'] = datetime.now().ctime()

                src = soup.select_one('.onair .article_link .article_img img')['src']
                self.dataset['imgDataSrc'] = replace_ascii(src).split('src="')[-1].split('"&')[0]
                self.dataset['liveDataHref'] = soup.select_one('.onair .article_link')['href']
                self.dataset['liveDataTitle'] = soup.select_one('.onair .article_link .title').text
                self.dataset['liveAttdc'] = int(soup.select_one('.onair .article_link .info.chat').text.replace('chat count','').replace('K','000'))
            
                self.dataset['category'], self.dataset['detail'] = parse_category(self.platform)
            else:
                self.dataset['_uniq'] = self.platform + self.channelID

                self.dataset['channel'] = self.channel
                self.dataset['platform'] = self.platform
                self.dataset['channelID'] = self.channelID

                self.dataset['onLive'] = False
                self.dataset['updateDate'] = datetime.now().ctime()
                
            driver.quit()
        except:
            driver.quit()

    def youtube(self):

        url, _ = platform_headers(self.platform, self.channelID)
        urldata = requests.get(url + '/channel/' + self.channelID, timeout=5)

        if urldata.status_code == 200:
            soup = BeautifulSoup(urldata.text, 'html.parser')
            link = soup.select('div.yt-lockup-dismissable')

            try:
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
                    self.dataset['creatorDataLogo'] = soup.select_one('.channel-header-profile-image')['src']

                    self.dataset['onLive'] = True
                    self.dataset['updateDate'] = datetime.now().ctime()
                    
                    self.dataset['imgDataSrc'] = link[0].select_one('div.yt-lockup-thumbnail > span > a > span > span > span > img').attrs['data-thumb']
                    self.dataset['liveDataHref'] = url + liveData.attrs['href']
                    self.dataset['liveDataTitle'] = liveData.attrs['title']
                    self.dataset['liveAttdc'] = int(AttdData.text.partition('명')[0].replace(',',''))

                    self.dataset['category'], self.dataset['detail'] = parse_category(self.platform, self.channelID)
                else :
                    self.dataset['_uniq'] = self.platform + self.channelID

                    self.dataset['channel'] = self.channel
                    self.dataset['channelID'] = self.channelID
                    self.dataset['platform'] = self.platform

                    self.dataset['onLive'] = False
                    self.dataset['updateDate'] = datetime.now().ctime()
            except:
                self.dataset['_uniq'] = self.platform + self.channelID

                self.dataset['channel'] = self.channel
                self.dataset['channelID'] = self.channelID
                self.dataset['platform'] = self.platform

                self.dataset['onLive'] = False
                self.dataset['updateDate'] = datetime.now().ctime()
        else:
            print(self.platform, self.channelID, urldata.status_code)

    def twitch(self):

        url, headers = platform_headers(self.platform, self.channelID, auth = self.auth)
        urldata = requests.get(url + self.channelID, headers=headers)
        creatorDataLogo = requests.get('https://api.twitch.tv/helix/users?login=' + self.channelID, headers=headers).json()

        if urldata.status_code == 200:
            urlJsonData = json.loads(urldata.text)
            
            if urlJsonData != {'data': [], 'pagination': {}} :
                self.dataset['_uniq'] = self.platform + self.channelID

                self.dataset['channel'] = self.channel
                self.dataset['channelID'] = self.channelID
                self.dataset['platform'] = self.platform
                self.dataset['creatorDataHref'] = "http://twitch.tv/" + self.channelID
                self.dataset['creatorDataName'] = urlJsonData['data'][0]['user_name']
                self.dataset['creatorDataLogo'] = creatorDataLogo['data'][0]['profile_image_url']

                self.dataset['onLive'] = True
                self.dataset['updateDate'] = datetime.now().ctime()

                self.dataset['imgDataSrc'] = urlJsonData['data'][0]['thumbnail_url'].replace('{width}', '356').replace('{height}', '200')
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
            print(self.platform, self.channelID, urldata.status_code)

    def afreecatv(self):
        
        url, headers = platform_headers(self.platform, self.channelID)
        urldata = requests.get(url, headers=headers)

        if urldata.status_code == 200:
            urlJsonData=json.loads(urldata.text)

            if urlJsonData['broad']:
                self.dataset['_uniq'] = self.platform + self.channelID

                self.dataset['channel'] = self.channel
                self.dataset['platform'] = self.platform
                self.dataset['channelID'] = self.channelID
                self.dataset['creatorDataHref'] = "http://bj.afreecatv.com/" + self.channelID
                self.dataset['creatorDataName'] = urlJsonData['station']['user_nick']
                self.dataset['creatorDataLogo'] = "http://stimg.afreecatv.com/LOGO/" + self.channelID[:2] + "/"+ self.channelID + "/"+ self.channelID + ".jpg"

                self.dataset['onLive'] = True
                self.dataset['updateDate'] = datetime.now().ctime()
                self.dataset['imgDataSrc'] = "//liveimg.afreecatv.com/" + str(urlJsonData['broad']['broad_no']) + "_480x270.gif"
                self.dataset['liveDataHref'] = "http://play.afreecatv.com/" + self.channelID + "/" + str(urlJsonData['broad']['broad_no'])
                self.dataset['liveDataTitle'] = urlJsonData['broad']['broad_title']
                self.dataset['liveAttdc'] = urlJsonData['broad']['current_sum_viewer']

                self.dataset['category'], self.dataset['detail'] = parse_category(self.platform, self.channelID)
            else :
                self.dataset['_uniq'] = self.platform + self.channelID

                self.dataset['channel'] = self.channel
                self.dataset['platform'] = self.platform
                self.dataset['channelID'] = self.channelID

                self.dataset['onLive'] = False
                self.dataset['updateDate'] = datetime.now().ctime()
        else:
            print(self.platform, self.channelID, urldata.status_code)

def multiprocess(target):
    crl = LiveCrawling()
    return crl.crawling(target=target)

def crawl_target(platform, mongo_auth):
    conn = MongoClient('mongodb://%s:%s@%s:%s' % (mongo_auth['username'], mongo_auth['password'], mongo_auth['hostname'], mongo_auth['port']),
                connect=False)
    db = conn['meerkatonair']
    collection = db['live_list']
    conn.close()

    if platform == 0:
        return collection.find({"platform": {"$in" : ["twitch","youtube","afreecatv"]}})
    elif platform == 1:
        return collection.find({"platform": "vlive"})
    else:
        return False
 
def mongo_insert(mongo_auth, results):
    conn = MongoClient('mongodb://%s:%s@%s:%s' % (mongo_auth['username'], mongo_auth['password'], mongo_auth['hostname'], mongo_auth['port']),
            connect=False)
    db = conn['meerkatonair']
    collection = db['live_list']

    success = len(results)
    for result in results:
        if result != None:
            platform, channelID, data = result
            if not data == {}:
                post_id = collection.update_one({'_uniq': platform + channelID}, {"$set": data}, upsert=True)
                print(platform.upper(), channelID, 'UPDATED')
            else:
                success -= 1
                print(platform.upper(), channelID, 'NOT UPDATED')

    print("SUCCESS [%d/%d]" %(success, len(results)))
    conn.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--platform', required=False, type=int, default=0, help="Define target platform [0: requests, 1: selenium]")
    parser.add_argument('--process', required=False, type=int, default=16, help="Define multiprocess worker")
    args = parser.parse_args()

    with open('mongodb_auth.json', 'r') as f:
        mongo_auth = json.load(f)
    
    target = crawl_target(args.platform, mongo_auth)
    pool = Pool(processes=args.process)

    s = time.time()    
    results = pool.map(multiprocess,[list(i.items()) for i in list(target)])
    mongo_insert(mongo_auth, results)
    print('Total : ', time.time() -s)
