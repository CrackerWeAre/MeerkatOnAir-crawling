import requests
from bs4 import BeautifulSoup

channelID = 'UC5F_d3cnqsl_6syKejWVWxw'

url = 'http://play.afreecatv.com/dldudgp2/station'

res =requests.get(url)

soup = BeautifulSoup(res.text, 'html.parser')
print(soup)