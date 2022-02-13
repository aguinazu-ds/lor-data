import json
import requests
import time
from read_write_delete_duplicates import readData, writeData, delete_duplicates_list
from ratelimit import limits, RateLimitException, sleep_and_retry
from api_token import api_token_var_list

print('Cargando match list desde data/lor-match-data/match-lists/...')
match_list = readData('data/lor-match-data/match-lists/match_list-20220211-233732.json')

TWO_MINUTES = 120
MAX_CALLS_PER_MINUTE= 100

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=TWO_MINUTES)
def get_match_info_by_id(region, match_id, api_key):
    api_url = 'https://{}.api.riotgames.com/lor/match/v1/matches/{}?api_key={}'.format(region, match_id, api_key)
    response = requests.get(api_url)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return response.status_code

counter=0
api_key_index = 0
temp_list = []
for i in range(len(api_token_var_list)):
    temp_list.append({'{}'.format(api_token_var_list[i]) : []})
set_time = time.strftime("%Y%m%d-%H%M%S")
print(temp_list)
print('Comenzando recolección de datos...')
for match in match_list:
    counter= counter +1
    try:
        match_info = get_match_info_by_id('americas', match, api_token_var_list[api_key_index])
        if match_info == 429:
            api_key_index += 1
            print('Error en paso {}'.format(counter))
            if api_key_index > len(api_token_var_list)-1:
                print('No me quedan más API Keys')
                break
            print('Error 429, cambiando API Key a {}'.format(api_token_var_list[api_key_index]))
        elif match_info == 404:
            print('Error en paso {}'.format(counter))
            print('Error 404, no se encontro información relacionada al id {}'.format(match))
            pass
        elif match_info["info"]["game_type"] == "Ranked" or match_info["info"]["game_mode"] == "SeasonalTournamentLobby":
            print('Guardando datos relacionados al id: {}'.format(match))
            temp_list[api_key_index][api_token_var_list[api_key_index]].append(match_info)
            writeData('data/lor-match-data/match_data-{}.json'.format(set_time), temp_list)
    except:
        print('Error en paso {}, no tengo idea que error!!!'.format(counter))