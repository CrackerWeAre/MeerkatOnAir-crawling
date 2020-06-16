import requests
from bs4 import BeautifulSoup
import urllib.request

channelID = 'UCR9gReM5VhQ_8brqQrBaVCA'
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
        }

url = 'https://www.youtube.com'

print(urllib.request.urlopen(url + '/channel/' + channelID).read())

# urldata = requests.get(url + '/channel/' + channelID, headers=headers)
# if urldata.status_code == 200:
#     soup = BeautifulSoup(urldata.text, 'html.parser')

#     imgDataSrc = soup.select_one('ytd-channel-featured-content-renderer > #contents > ytd-video-renderer > #dismissable > ytd-thumbnail > a > yt-img-shadow > img')


    



    # dataLiveConfirm = linkData[0].select_one('a')['data-sessionlink']

    # if dataLiveConfirm.find('live') > 0 :
    # liveData = link[0].select_one('div.yt-lockup-content > h3 > a')
    # AttdData = link[0].select_one('div.yt-lockup-content > div.yt-lockup-meta > ul > li ')
    # creatorData = link[0].select_one('div.yt-lockup-content > div.yt-lockup-byline > a')

    # self.dataset['_uniq'] = self.platform + self.channelID

    # self.dataset['channel'] = self.channel
    # self.dataset['channelID'] = self.channelID
    # self.dataset['platform'] = self.platform
    # self.dataset['creatorDataHref'] = url + creatorData.attrs['href']
    # self.dataset['creatorDataName'] = creatorData.text
    # self.dataset['creatorDataLogo'] = soup.select_one('.channel-header-profile-image')['src']

    # self.dataset['onLive'] = True
    # self.dataset['updateDate'] = datetime.now().ctime()
    
    # self.dataset['imgDataSrc'] = link[0].select_one('div.yt-lockup-thumbnail > span > a > span > span > span > img').attrs['data-thumb']
    # self.dataset['liveDataHref'] = url + liveData.attrs['href']
    # self.dataset['liveDataTitle'] = liveData.attrs['title']
    # self.dataset['liveAttdc'] = int(AttdData.text.partition('명')[0].replace(',',''))

    # self.dataset['category'], self.dataset['detail'] = parse_category(self.platform, self.channelID)



