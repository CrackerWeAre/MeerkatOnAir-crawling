import requests
import json
from bs4 import BeautifulSoup

import re


channelID = 'UCsOW9TPy2TKkqCchUHL04Fg'

res = requests.get('https://www.youtube.com/channel/' + channelID)
soup = BeautifulSoup(res.text, 'html.parser')

try:
    matched = re.search(r'window\[\"ytInitialData\"\] = (.+?)};', res.text, re.S)
    json_string = json.loads(matched.group(1)+'}')


    for k, v in json_string.items():
        if k == 'header':
            obj = v['c4TabbedHeaderRenderer']
            print(obj['channelId'])
            print(obj['title'])
            print(obj['avatar']['thumbnails'][0]['url'])
            print(obj['subscriberCountText']['runs'][0]['text'])

        elif k == 'metadata':
            obj = v['channelMetadataRenderer']
            print(obj['description'])
            # print(obj['keywords'])
            print(obj['channelUrl'])

        elif k == 'contents':
            try:
                obj = v['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][
                    0]['itemSectionRenderer']['contents'][0]['channelFeaturedContentRenderer']['items'][0]['videoRenderer']
                print(obj['videoId'])
                print(obj['thumbnail']['thumbnails'][-1]['url'])
                print(obj['title']['simpleText'])
                print(obj['viewCountText']['runs'][0]['text'])
                print(obj['badges'][0]['metadataBadgeRenderer']['style'])
                print(obj['badges'][0]['metadataBadgeRenderer']['label'])
            except KeyError:
                print("no live")

except Exception as e:
    print(e)