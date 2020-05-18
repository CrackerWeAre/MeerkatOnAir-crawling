import requests
from bs4 import BeautifulSoup

channelID = 'UC5F_d3cnqsl_6syKejWVWxw'

url = 'http://play.afreecatv.com/dldudgp2/223822478'

res =requests.get(url)

soup = BeautifulSoup(res.text, 'html.parser')
print(soup.select_one('.detail_view'))