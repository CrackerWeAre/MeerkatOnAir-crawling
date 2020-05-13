from requests_utils import platform_headers
from selenium.webdriver.chrome import webdriver, options

from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime

platform = 'vlive'
channelID = 'DE341F'
channel = 'itzy'

dataset ={}

driver = webdriver.WebDriver('driver/chromedriver.exe')

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


print(dataset)
driver.quit()