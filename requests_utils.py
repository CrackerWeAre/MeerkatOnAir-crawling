import requests
import json 

def replace_ascii(string):
    string = string.replace('%22','"')
    string = string.replace('%3A',':')
    string = string.replace('%2F','/')
    string = string.replace('%3F','?')
    string = string.replace('%3D','=')
    return string

def platform_headers(platform, channelID, auth = None):
    
    if platform == 'afreecatv':
        url = "http://bjapi.afreecatv.com/api/" + channelID + "/station/"

        headers = { "Host": "bjapi.afreecatv.com",
                    "Origin": "http://bj.afreecatv.com",
                    "Referer": "http://bj.afreecatv.com/" + channelID,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
                    "Content-Type": "application/json"}
    
    elif platform == 'twitch':
        url = "http://api.twitch.tv/helix/streams?user_login="
        headers = {
            "Client-ID": auth[platform]['Client-ID'],
            "Accept": "application/vnd.twitchtv.v5+json",
            "Authorization": "Bearer " + auth[platform]['Authorization'] 
            }

    elif platform == 'youtube':
        url = "https://www.youtube.com"
        headers = {}

    elif platform == 'vlive':
        url = "https://channels.vlive.tv/" + channelID + '/home'
        headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
                }

    return url, headers

def parse_category(platform, id=None, headers=None):
    with open('data/id2cat.json') as f:
        id2cat = json.load(f)

    if platform == 'afreecatv':
        try:
            category = id2cat[id]['category']
            detail = id2cat[id]['category-detail']
        except KeyError:
            category, detail = '', ''
    
    elif platform == 'twitch':
        
        if id == '26936':
            category = 'MUSIC'
            detail = ''
        elif id == '509667':
            category = 'CHATTING'
            detail = 'Food & Drink'
        elif id == '509658':
            category = 'CHATTING'
            detail = ''
        elif id == '517249':
            category = 'SPORTS & EXERCISE'
            detail = 'SPORTS'
        elif id == '509671':
            category = 'SPORTS & EXERCISE'
            detail = 'EXERCISE'
        else:
            category = 'GAME'
            detail = requests.get('https://api.twitch.tv/helix/games?id='+str(id) , headers=headers).json()['data'][0]['name']

    elif platform == 'youtube':
        try:
            category = id2cat[id]['category']
            detail = id2cat[id]['category-detail']
        except KeyError:
            category, detail = '', ''
    elif platform == 'vlive':
        category = 'CHATTING'
        detail = ''

    return category, detail
