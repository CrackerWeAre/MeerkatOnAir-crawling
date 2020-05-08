import json

with open('target.json', 'r', encoding='utf-8') as f:
    j = json.load(f)

for platform, value in j.items():
    for k,v in value.items():
        data = {
            'platform' : platform,
            'channel' : k,
            'channelID' : v
        }
        with open(k +'.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
            