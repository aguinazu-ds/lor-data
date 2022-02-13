import json
import requests
import time
from read_write_delete_duplicates import readData, writeData, delete_duplicates_list
from ratelimit import limits, RateLimitException, sleep_and_retry
from api_token import api_token_var_list
from get_player_puuid import get_player_puuid

print('Cargando Base de datos...')
print("\n")

master_player_list = readData('data/lor-player-data/master_player_list.json')

print('Base de datos Cargada.')
print("\n")

match_list = []

@sleep_and_retry
@limits(calls=1, period=2)
def get_player_match_list(region, ppuid, api_key):
    api_url = 'https://{}.api.riotgames.com/lor/match/v1/matches/by-puuid/{}/ids?api_key={}'.format(region, ppuid, api_key)
    respuesta = requests.get(api_url)
    if respuesta.status_code == 200:
        return json.loads(respuesta.content.decode('utf-8'))
    else:
        return respuesta.status_code

print('Iniciando recolección de datos...')
print("\n")

counter = 0
api_key_index_player_ppuid = 0
api_key_index_match_list = 9

for player in master_player_list:
    counter += 1
    try:
        player_ppuid = get_player_puuid('americas', player['gameName'], player['tagLine'], api_token_var_list[api_key_index_player_ppuid])
        if player_ppuid == 429:
            api_key_index_player_ppuid += 1
            if api_key_index_player_ppuid > len(api_token_var_list)-1:
                print('No me quedan más API Keys')
                break
            else:
                print('Error 429 en el paso {}, en el bloque player_ppuid, cambiando API Key a {}'.format(counter,api_token_var_list[api_key_index_player_ppuid]))
                print('Intentando denuevo en el paso {}'.format(counter))
                player_ppuid = get_player_puuid('americas', player['gameName'], player['tagLine'], api_token_var_list[api_key_index_player_ppuid])
                print("\n")
        else:
            print('Recolectando match list relacionada al siguiente jugador: {}'.format(player))
            try:
                new_matches = get_player_match_list('americas', player_ppuid, api_token_var_list[api_key_index_player_ppuid])
                if  new_matches == 429:
                    api_key_index_match_list -= 1
                    print('Error en paso {}'.format(counter))
                    if api_key_index_match_list == -1:
                        print('No me quedan más API Keys')
                        break
                    else:
                        print('Error 429, en el bloque de match list, cambiando API Key a {}'.format(api_token_var_list[api_key_index_match_list]))
                        print('Probando con nueva API Key en el paso {}'.format(counter))
                        new_matches = get_player_match_list('americas', player_ppuid, api_token_var_list[api_key_index_match_list])
                        match_list = match_list + new_matches
                        print("\n")
                else:
                    match_list = match_list + new_matches
            except:
                print("\n")
                print('Error en paso {}, no tengo idea que error!!!, pero puede ser Error {}'.format(counter, new_matches))
                print("\n")
    except:
        print("\n")
        print('Error en paso {}, no tengo idea que error!!!, pero puede ser Error {}'.format(counter, player_ppuid))
        print("\n")

print("\n")
print('Recolección de datos terminada...')
print('Guardando datos en data/lor-match-data/match-lists/...')
set_time = time.strftime("%Y%m%d-%H%M%S")
writeData('data/lor-match-data/match-lists/master-match_list-{}.json'.format(set_time),delete_duplicates_list(match_list))