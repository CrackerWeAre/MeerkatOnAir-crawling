from requests_utils import platform_headers

from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime

platform = "twitch"
channelID = "kimdoe"

auth = {
    'twitch' : {
        "Client-ID" : "gp762nuuoqcoxypju8c569th9wz7q5",
        "Authorization" : "dai8zvcrkdjpicilbj2nnbc6k8il2r"
    }
}

url, headers = platform_headers(platform, channelID, auth = auth)
# urldata = requests.get(url + channelID, headers=headers)


res = requests.get('https://api.twitch.tv/helix/games?id='+str(509538) , headers=headers).json()['data'][0]['name']

print(res)