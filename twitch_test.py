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

if __name__ == "__main__":

    res = requests.get('https://api.twitch.tv/helix/games?id='+str(509671) , headers=headers).json()
    print(res)
    
    #res = requests.get('https://api.twitch.tv/helix/users?login=yagubu', headers=headers)

    # res = requests.get('http://api.twitch.tv/helix/streams?user_login=hochschulsport_goettingen', headers=headers)
    # print(res.json())
    