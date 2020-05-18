import requests
from bs4 import BeautifulSoup

channelID = 'UC5F_d3cnqsl_6syKejWVWxw'

url = 'https://www.youtube.com'

urldata = requests.get(url + '/channel/' + channelID)

if urldata.status_code == 200:
    soup = BeautifulSoup(urldata.text, 'html.parser')
    link = soup.select('div.yt-lockup-dismissable')
    linkData =  link[0].select('div.yt-lockup-content')
    dataLiveConfirm = linkData[0].select_one('a')['data-sessionlink']

    if dataLiveConfirm.find('live') > 0 :
        liveData = link[0].select_one('div.yt-lockup-content > h3 > a')


res = requests.get(url + liveData['href'])

soup = BeautifulSoup(res.text, 'html.parser')
# text = soup.select_one('#content > yt-formatted-string > a').text
# print(text)

print(soup)