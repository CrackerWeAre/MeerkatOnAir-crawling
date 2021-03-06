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

headers = {
    "Client-ID": auth['twitch']['Client-ID'] ,
    "Accept": "application/vnd.twitchtv.v5+json",
    "Authorization": "Bearer %s" % auth['twitch']['Authorization'] 
    }

def subscription():
    
    res = requests.get("https://api.twitch.tv/helix/users/follows", params={
        'to_id': 36473331,
    }, headers=headers)

    print(res.json()['total'])


def twitchAll():
    max_results = 5
    streams = []
    pagination = ''

    while len(streams) <= max_results:
        responseTwitch = requests.get("https://api.twitch.tv/helix/streams", params={
            "first": 2,
            "after": pagination,
        }, headers=headers)

        print(responseTwitch)

        streams.append(responseTwitch.json()['data'])
        # pagination = responseTwitch.json()['pagination']['cursor']

    print(streams)


if __name__ == "__main__":
    subscription()