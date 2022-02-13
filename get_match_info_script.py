import json
import requests
import time
from read_write_delete_duplicates import readData, writeData, delete_duplicates_list
from ratelimit import limits, RateLimitException, sleep_and_retry
from api_token import api_token_var_list

print('Cargando match list desde data/lor-match-data/match-lists/...')
print("\n")
match_list = readData('data/lor-match-data/match-lists/master-match_list-20220212-232705.json')

TWO_MINUTES = 2
MAX_CALLS_PER_MINUTE= 1

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=TWO_MINUTES)
def get_match_info_by_id(region, match_id, api_key):
    api_url = 'https://{}.api.riotgames.com/lor/match/v1/matches/{}?api_key={}'.format(region, match_id, api_key)
    response = requests.get(api_url)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8')), response
    else:
        return response.status_code, response

counter=0
api_key_index = 0
temp_list = []

for i in range(len(api_token_var_list)):
    temp_list.append({'{}'.format(api_token_var_list[i]) : []})

set_time = time.strftime("%Y%m%d-%H%M%S")

print('Comenzando recolección de datos...')
print("\n")
for match in match_list:
    counter= counter +1

    match_info = get_match_info_by_id('americas', match, api_token_var_list[api_key_index])

    if match_info[0] == 429:

        api_key_index += 1
        print("\n")
        print('Error en paso nº{}'.format(counter))
        print('Error 429, rate limit alcanzado:')
        print('{}'.format(match_info[1].headers["X-App-Rate-Limit-Count"]))
        print('{}'.format(match_info[1].headers["X-Method-Rate-Limit-Count"]))
        print("\n")
        print('Cambiando API Key a {}'.format(api_token_var_list[api_key_index]))

        if api_key_index > len(api_token_var_list)-1:
            print("\n")
            print('No me quedan más API Keys')
            print('Terminamos en el paso nº{}'.format(counter))
            break
        else:
            match_info = get_match_info_by_id('americas', match, api_token_var_list[api_key_index])            
            print("\n")
            print('Intentando denuevo el paso nº{}...'.format(counter))
            print('Guardando datos relacionados al id: {}'.format(match))
            temp_list[api_key_index][api_token_var_list[api_key_index]].append(match_info[0])
            writeData('data/lor-match-data/match_data-{}.json'.format(set_time), temp_list)

    elif match_info[0] == 404:
        print("\n")
        print('Error en paso nº{}'.format(counter))
        print('Error 404, no se encontro información relacionada al id {}'.format(match))
        pass

    elif match_info[0]["info"]["game_type"] == "Ranked" or match_info[0]["info"]["game_mode"] == "SeasonalTournamentLobby":
        print('Guardando datos relacionados al id: {}'.format(match))
        temp_list[api_key_index][api_token_var_list[api_key_index]].append(match_info[0])
        writeData('data/lor-match-data/match_data-{}.json'.format(set_time), temp_list)