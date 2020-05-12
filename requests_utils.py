
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
            "Accept": "application/vnd.twitchtv.v5+json"
            }

    elif platform == 'youtube':
        url = "https://www.youtube.com"
        headers = {}

    return url, headers