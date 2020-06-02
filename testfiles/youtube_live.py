import requests
from bs4 import BeautifulSoup

url = 'http://www.youtube.com' + '/watch?v=CfX5IWY-rE0'

res = requests.get(url)

soup = BeautifulSoup(res.text, 'html.parser')

print(soup)
