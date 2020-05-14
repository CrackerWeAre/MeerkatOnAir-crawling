from requests_utils import platform_headers
from selenium import webdriver

from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime

platform = 'vlive'
channelID = 'DED40B'
channel = '엘리스'

dataset ={}
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-extensions')
options.add_argument('--no-sandbox')
#options.add_argument('window-size=1920x1080')
#options.add_argument("disable-gpu")
#options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")

driver = webdriver.Chrome('driver/chromedriver', options=options)

url, _ = platform_headers(platform, channelID)

driver.get(url)
time.sleep(0.5)
soup = BeautifulSoup(driver.page_source, 'html.parser')

onair = soup.select_one('.onair')
if not soup.select_one('.onair') == None:
    dataset['onLive'] = True
    dataset['_id'] = channelID
    dataset['channel'] = channel
    dataset['platform'] = platform

    dataset['creatorDataHref'] = url
    dataset['creatorDataName'] = soup.select_one('.channel_info_area .name').text

    dataset['updateDate'] = datetime.now().ctime()

    dataset['imgDataSrc'] = soup.select_one('.onair .article_link .article_img img')['src']
    dataset['liveDataHref'] = soup.select_one('.onair .article_link')['href']
    dataset['liveDataTitle'] = soup.select_one('.onair .article_link .title').text
    dataset['liveAttdc'] = soup.select_one('.onair .article_link .info.chat').text
else:
    dataset['onLive'] = False
    dataset['_id'] = channelID
    dataset['channel'] = channel
    dataset['platform'] = platform
    dataset['updateDate'] = datetime.now().ctime()


print(dataset)
driver.quit()
