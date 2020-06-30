import requests


DEVELOPER_KEY = "AIzaSyATi0yW-mcW9vCxMwg0fqOmbkANkKODm3Q"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def getChannel(channelID, youtubeAuth):
    url = "https://www.googleapis.com/youtube/v3/channels"
    return requests.get(url, params={
        'part':'snippet',
        'id': channelID,
        'key': youtubeAuth['APIKEY']})

def getLiveStreams(channelID, youtubeAuth):
    url = "https://www.googleapis.com/youtube/v3/search?"
    return requests.get(url, params={
    'part': 'snippet',
    'eventType': 'live',
    'type': 'video',
    # 'channelId': channelID,
    'key': youtubeAuth['APIKEY']})

# channel = getChannel(channelID="UCsOW9TPy2TKkqCchUHL04Fg", youtubeAuth=youtubeAuth).json()['items'][0]['snippet']


# channelTitle = channel['title']
# channelDescription = channel['description']
# channelPublishedAt = channel['publishedAt']
# channelThumbnails = channel['thumbnails']
# channelCountry = channel['country']

print(getLiveStreams(channelID="UCsOW9TPy2TKkqCchUHL04Fg", youtubeAuth=youtubeAuth).text)


