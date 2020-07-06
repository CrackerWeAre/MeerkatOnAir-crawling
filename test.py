import requests
import json
from bs4 import BeautifulSoup

import re


channelID = 'UCX2laRqGQhqoChYmlaUgOiw'

res = requests.get('https://www.youtube.com/channel/' + channelID, timeout=5)
soup = BeautifulSoup(res.text, 'html.parser')

link = soup.select('div.yt-lockup-dismissable')
print(soup)