import requests
import json
from bs4 import BeautifulSoup

import re


with open ('UCs0LzOveQMLImmmTrMmP2sg.txt', 'r', encoding='utf-8') as f:
    text = f.read()

matched = re.search(r'window\[\"ytInitialData\"\] = (.+?)};', text, re.S)
# matched = re.search(r'var ytInitialData = (.+?)};', text, re.S)
# json_string = json.loads(matched.group(1)+'}')

print(matched== None)