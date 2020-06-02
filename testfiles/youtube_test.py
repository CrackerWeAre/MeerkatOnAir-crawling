import requests
from bs4 import BeautifulSoup

channelID = 'UCsOW9TPy2TKkqCchUHL04Fg'

url = 'https://www.youtube.com'

urldata = requests.get(url + '/channel/' + channelID)

if urldata.status_code == 200:
    soup = BeautifulSoup(urldata.text, 'html.parser')
    link = soup.select('div.yt-lockup-dismissable')
    linkData =  link[0].select('div.yt-lockup-content')
    dataLiveConfirm = linkData[0].select_one('a')['data-sessionlink']

    if dataLiveConfirm.find('live') > 0 :
        liveData = link[0].select_one('div.yt-lockup-content > h3 > a')
        AttdData = link[0].select_one('div.yt-lockup-content > div.yt-lockup-meta > ul > li ')

        print(liveData)
    #print(soup.select_one('.channel-header-profile-image')['src'])
