import json
import requests

api_token = 'RGAPI-2a309c08-fd0c-4bbf-9359-5e84a73f2563'
check = requests.get('https://americas.api.riotgames.com/lor/ranked/v1/leaderboards?api_key={}'.format(api_token))

def get_ranked_info(region):
    ''' '''
    api_url_base = 'https://{}.api.riotgames.com/lor/ranked/v1/leaderboards'
    api_url = '{}?api_key={}'.format(api_url_base.format(region),api_token)
    respuesta = requests.get(api_url)

    if respuesta.status_code == 200:
        return json.loads(respuesta.content.decode('utf-8'))
    else:
        return None

if check.status_code == 200:
    data_americas, data_europe, data_sea = get_ranked_info('americas'), get_ranked_info('europe'), get_ranked_info('sea')
    with open('data/master-leaderboard-data/data_americas.json', 'w', encoding='utf-8') as f:
        json.dump(data_americas, f, ensure_ascii=False, indent=4)
    with open('data/master-leaderboard-data/data_europe.json', 'w', encoding='utf-8') as f:
        json.dump(data_europe, f, ensure_ascii=False, indent=4)
    with open('data/master-leaderboard-data/data_sea.json', 'w', encoding='utf-8') as f:
        json.dump(data_sea, f, ensure_ascii=False, indent=4)
else:
    print(check.status_code)
    print('Revisa tu token API o ve si hay otro problema con los servidores de Riot')