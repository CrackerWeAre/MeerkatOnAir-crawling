import requests
import requests
import json
import time
import pymongo
import argparse
from bs4 import BeautifulSoup

channelID = 'UCGKQ4Tw5nPXMGsoYZHrHYeA'

urldata = requests.get('https://www.youtube.com' + '/channel/' + channelID, timeout=5)

if urldata.status_code == 200:
    soup = BeautifulSoup(urldata.text, 'html.parser')
    link = soup.select('#badges > div > span')

    with open('res.txt', 'w') as f:
        f.write(soup.get_text())