import json
import requests
from ratelimit import limits, RateLimitException, sleep_and_retry
from api_token import api_token_var


def readData(filename):
    data = None
    with open(filename, 'r') as fp:
        data = json.load(fp)
    return data

master_player_list = readData('data/lor-player-data/master_player_list_ppuids.json')

match_list = []

TWO_MINUTES = 120
MAX_CALLS_PER_MINUTE= 99

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=TWO_MINUTES)
def get_player_match_list(region, ppuid, api_key):
    api_url = 'https://{}.api.riotgames.com/lor/match/v1/matches/by-puuid/{}/ids?api_key={}'.format(region, ppuid, api_key)
    respuesta = requests.get(api_url)
    return json.loads(respuesta.content.decode('utf-8'))

for player in master_player_list:
    match_list = match_list + get_player_match_list('americas', player, api_token_var)


