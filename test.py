import requests
import json
from bs4 import BeautifulSoup

import re


with open ('UC1p5kp09LAS3kpQB3O8YQJw.json', 'r', encoding='utf-8') as f:
    jd = json.load(f)


print(jd['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['channelVideoPlayerRenderer'].keys())