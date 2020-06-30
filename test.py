import requests
import requests
import json
import time
import pymongo
import argparse
from bs4 import BeautifulSoup

channelID = 'UCvdwhh_fDyWccR42-rReZLw'

urldata = requests.get('https://www.youtube.com' + '/channel/' + channelID, timeout=5)

if urldata.status_code == 200:
    soup = BeautifulSoup(urldata.text, 'html.parser')
    link = soup.select('div.yt-lockup-dismissable')

    print(soup)
    try:
        linkData =  link[0].select('div.yt-lockup-content')
        dataLiveConfirm = linkData[0].select_one('a')['data-sessionlink']
    except Exception as e:
        print(e)