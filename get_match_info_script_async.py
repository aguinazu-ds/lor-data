import json
import requests
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

print('Cargando match list desde data/lor-match-data/match-lists/...')
print("\n")

# Cargamos el archivo que contiene los match ids de los que queremos obtener información
match_list = readData('data/lor-match-data/match-lists/master-match_list-20220212-232705.json')
match_list_test= match_list[:1000] #Conjunto de prueba con los primeros 1000 ids (En total son mas de 6000 ids)


async def main():
    async with aiohttp.ClientSession() as session:

        tasks = []

        # Iteramos por todas las API Keys que tenemos. Estas keys están guardadas en el archivo api_token.py (Son 21 keys)
        for key in api_token_var_list:
            task = asyncio.ensure_future(get_match_info(session, key, api_token_var_list.index(key)))
            tasks.append(task)

        data = await asyncio.gather(*tasks)
        writeData('data/lor-match-data/match_data-{}.json'.format(set_time), flatten(data))


# Función que queremos correr de manera asincronica, sin esperar a que cada API call termine.
async def get_match_info(session, keys, index):

    #hundred_match_list = match_list[4193+100*index:]

    #
    @sleep_and_retry
    @limits(calls=1, period=1.5)
    async def get_match_info_by_id(match_id, api_key):
        api_url = 'https://{}.api.riotgames.com/lor/match/v1/matches/{}?api_key={}'.format('americas', match_id, api_key)
        async with session.get(api_url) as response:
            # result = response
            if response.status == 200:
                return await response.json(encoding='utf-8')
            else:
                return response.status
    
    # Contador paa saber en que id de la match list obtivimos algún error
    counter=0

    temp_list = []

    temp_list.append({'{}'.format(api_token_var_list[index]) : []})

    for id_index in range(len(match_list_test)):
        counter= counter +1

        if (21*id_index + index) > len(match_list_test) -1:
            return temp_list

        match_info = await get_match_info_by_id(match_list[21*id_index + index], api_token_var_list[index])

        # if (match_info["info"]["game_type"] == "Ranked") or (match_info["info"]["game_mode"] == "SeasonalTournamentLobby"):
        #     print('Guardando datos relacionados al id: {}'.format(match))
        #     temp_list[index][api_token_var_list[index]].append(match_info)

        # · El error 429, es cuando pasamos alguno de los limites que impone Riot al hacer API Calls.
        # Para las API Keys que tengo yo (21 keys), cada una tiene un límite de 1 llamada cada 20seg o 100 llamadas cada 120 seg.
        # Además, cada tipo de llamada tiene su límite, en el caso de esta función, cuando llamamos a la URL de riot para obtener
        # información (linea 48 y 49), este método en particular tiene un límite de 100 llamadas cada una hora.
        # · El error 400 es cuando no se encuentra información (en los servidores de Riot) asociada a el match id solicitado.
        if match_info == 429: 
            print(counter)
            print(match_info)
            return temp_list
        elif match_info == 400:
            print(counter)
            print(match_info)
            pass
        else:
            print('Guardando datos relacionados al id: {}'.format(match_list_test[id_index]))
            temp_list[0][api_token_var_list[index]].append(match_info)
    
    return temp_list


asyncio.run(main())