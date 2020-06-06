import requests
from bs4 import BeautifulSoup

url = 'http://www.youtube.com' + '/watch?v=CfX5IWY-rE0'

IDs = ['https://www.youtube.com/watch?v=Dx5qFachd3A','https://www.youtube.com/watch?v=maGlNetcuPM','https://www.youtube.com/watch?v=ifVFayN6N0k',
        'https://www.youtube.com/watch?v=U_sYIKWhJvk','https://www.youtube.com/watch?v=VN0WDA8sh4s','https://www.youtube.com/watch?v=e6iGJIYUroo']

for url in IDs:

    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')
    try:
        print(soup.select('.yt-uix-sessionlink.spf-link')[3])
    except:
        pass
