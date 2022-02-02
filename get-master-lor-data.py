import json
from urllib import response
import requests

api_token = 'RGAPI-2a309c08-fd0c-4bbf-9359-5e84a73f2563'
api_url_base = 'https://americas.api.riotgames.com/lor/ranked/v1/leaderboards'

response = requests.get('{}?api_key={}'.format(api_url_base,api_token))

def get_ranked_info():
    ''' '''
    api_url = '{}?api_key={}'.format(api_url_base,api_token)
    response = requests.get(api_url)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

data = get_ranked_info()

with open('data/data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
