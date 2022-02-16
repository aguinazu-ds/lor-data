import time
import aiohttp
import asyncio
from read_write_delete_duplicates import readData, writeData, delete_duplicates_list
from ratelimit import limits, RateLimitException, sleep_and_retry
from api_token import api_token_var_list

# Función para transformar Lista de listas a una sola lista [[a],[b],[c]] ---> [a,b,c] 
def flatten(t):
    return [item for sublist in t for item in sublist]

# Fijamos el tiempo cuando se ejecutó el script para guardar el archivo con la info que se obtuvo, con fecha y hora.
set_time = time.strftime("%Y%m%d-%H%M%S")

americas_master_players = readData('data/lor-player-data/masterplayerlistAmericas.json')

async def main():
    async with aiohttp.ClientSession() as session:

        tasks = []

        # Iteramos por todas las API Keys que tenemos. Estas keys están guardadas en el archivo api_token.py (Son 21 keys)
        for key in api_token_var_list:
            task = asyncio.ensure_future(getMatchList(session, key, api_token_var_list.index(key)))
            tasks.append(task)
            print(tasks)

        data = await asyncio.gather(*tasks)
        writeData('data/lor-match-data/match-lists/master-match-list-{}.json'.format(set_time), flatten(data))

async def getMatchList(session, api_key, index):

    @sleep_and_retry
    @limits(calls=1, period=0.625)
    @limits(calls=1000, period=60)
    async def getPlayerPUUID(region, gameName, tagLine, api_key):
        api_url = 'https://{}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{}/{}?api_key={}'.format(region,gameName, tagLine, api_key)
        async with session.get(api_url) as response:
            if response.status == 200:
                return await response.json(encoding='utf-8'), response
            else:
                return response.status, response

    
    @sleep_and_retry
    @limits(calls=1, period=0.625)
    @limits(calls=200, period=3600)
    async def getMatchListbyPUUID(region, player_puuid, api_key):
        api_url = 'https://{}.api.riotgames.com/lor/match/v1/matches/by-puuid/{}/ids?api_key={}'.format(region, player_puuid, api_key)
        async with session.get(api_url) as response:
            if response.status == 200:
                return await response.json(encoding='utf-8'), response
            else:
                return response.status, response

    counter = 0
    temp_list = []

    for player_index in range(len(americas_master_players)):
        counter = len(api_token_var_list)*player_index + index + 1

        if (len(api_token_var_list)*player_index + index) > len(americas_master_players)-1:
            print('Termina API KEY {}'.format(api_key))
            break
        
        print('Buscando PUUID relacionado al jugador {}'.format(americas_master_players[len(api_token_var_list)*player_index + index]))
        player_puuid = await getPlayerPUUID('americas', americas_master_players[len(api_token_var_list)*player_index + index]['gameName'], americas_master_players[len(api_token_var_list)*player_index + index]['tagLine'], api_key)
        if player_puuid[0] == 429:
            print("\n")
            print('Error en paso nº{}'.format(counter))
            print('Error 429, rate limit alcanzado.')
            print('"X-App-Rate-Limit-Count": {}'.format(player_puuid[1].headers["X-App-Rate-Limit-Count"]))
            print('"X-Method-Rate-Limit-Count": {}'.format(player_puuid[1].headers["X-Method-Rate-Limit-Count"]))
            break
        elif player_puuid[0] == 404:
            print("\n")
            print('Error en paso nº{}'.format(counter))
            print('Error 404, no se encontro información relacionada al jugador {}'.format(americas_master_players[len(api_token_var_list)*player_index + index]))
            pass
        elif player_puuid[0] == 403:
            print("\n")
            print('Error 403 en paso nº{}'.format(counter))
            print('Revisar vigencia API Key {}'.format(api_token_var_list[index]))
            break
        else:
            print('Recolectando ids de los 20 últimas partidas de {}'.format(americas_master_players[len(api_token_var_list)*player_index + index]['gameName']))
            match_list = await getMatchListbyPUUID('americas', player_puuid[0]['puuid'], api_key)
            if match_list[0] == 429:
                print("\n")
                print('Error en paso nº{}'.format(counter))
                print('Error 429, rate limit alcanzado.')
                print('"X-App-Rate-Limit-Count": {}'.format(match_list[1].headers["X-App-Rate-Limit-Count"]))
                print('"X-Method-Rate-Limit-Count": {}'.format(match_list[1].headers["X-Method-Rate-Limit-Count"]))
                break
            elif match_list[0] == 404:
                print("\n")
                print('Error en paso nº{}'.format(counter))
                print('Error 404, no se encontro información relacionada al PUUID {}'.format(match_list[0]))
                pass
            elif match_list[0] == 403:
                print("\n")
                print('Error 403 en paso nº{}'.format(counter))
                print('Revisar vigencia API Key {}'.format(api_key))
                break
            else:
                temp_list = temp_list + match_list[0]

    return temp_list

asyncio.run(main())