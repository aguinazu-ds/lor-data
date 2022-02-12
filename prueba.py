import json
import requests
import time
from ratelimit import limits, RateLimitException, sleep_and_retry
from api_token import api_token_var


def readData(filename):
    data = None
    with open(filename, 'r') as fp:
        data = json.load(fp)
    return data
print('Cargando Base de datos...')
master_player_list = readData('data/lor-player-data/master_player_list_ppuids.json')

match_list = []

TWO_MINUTES = 120
MAX_CALLS_PER_MINUTE= 100

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=TWO_MINUTES)
def get_player_match_list(region, ppuid, api_key):
    api_url = 'https://{}.api.riotgames.com/lor/match/v1/matches/by-puuid/{}/ids?api_key={}'.format(region, ppuid, api_key)
    respuesta = requests.get(api_url)
    if respuesta.status_code == 200:
        return json.loads(respuesta.content.decode('utf-8'))
    else:
        return respuesta.status_code

print('Iniciando recolección de datos...')
for player in master_player_list:
    print('Recolectando match list relacionada al siguiente id: {}'.format(player))
    match_list = match_list + get_player_match_list('americas', player, api_token_var)

def writeData(filename, data):
    with open(filename, 'w') as file:
         file.write(format(json.dumps(data, ensure_ascii=False, indent=4)))

def delete_duplicates_list(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

print('Recolección de datos terminada...')
print('Guardando datos en data/lor-match-data/match-lists/...')
set_time = time.strftime("%Y%m%d-%H%M%S")
writeData('data/lor-match-data/match-lists/match_list-{}.json'.format(set_time),delete_duplicates_list(match_list))

